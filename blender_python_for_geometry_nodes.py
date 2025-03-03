import random
import time

import bpy

####################
# ヘルパー関数


def purge_orphans():
    """
    すべの孤立したデータブロックの削除
    参照:https://youtu.be/3rNqVPtbhzc?t=149
    """

    if bpy.app.version >= (3, 0, 0):
        # Blender バージョン3.0以降でのみ実行
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
    else:
        # Blender バージョン3.0未満でのみ実行
        # 削除する孤立したデータブロックがなくなるまで、
        # purge_orphans()を再帰的に呼び出す
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    """
    すべてのオブジェクト、コレクション、マテリアル、パーティクル、
    テクスチャ、イメージ、カーブ、メッシュ、アクション、ノード、
    ワールドをシーンから削除する
    参照:https://youtu.be/3rNqVPtbhzc
    """

    # アクティブなオブジェクトが編集モードになっていないことを確認する
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    # オブジェクトがビューポート非表示、選択無効化されていないかの確認
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # すべてのオブジェクトを選択して削除
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # すべてのコレクションを見つけて削除
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # ワールドシェーダーを変更する場合
    # ワールドオブジェクトを削除して再作成する
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # 新しいワールドデータブロックを作成
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    現在アクティブなオブジェクトを返す
    """

    return bpy.context.active_object


def time_seed():
    """
    時間に基づいてランダムシードを設定
    シードをクリップボードにコピー
    """

    seed = time.time()
    print(f"seed:{seed}")
    random.seed(seed)

    # シード値をクリップボードに追加
    bpy.context.window_manager.clipboard = str(seed)

    return seed


# アニメーションを線形補間に設定する関数
def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


# ループアニメーションを作成する関数
def create_data_animation_loop(
    obj,
    data_path,
    start_value,
    mid_value,
    start_frame,
    loop_length,
    linear_extrapolation=True,
):
    """
    データ プロパティ ループを作成するには、次の操作が必要
    1. プロパティを初期値に設定し、ループの先頭にキーフレームを追加
    2. プロパティを中間値に設定し、ループの途中にキーフレームを追加
    3. プロパティを初期値に設定し、ループの最後にキーフレームを追加
    """

    # 開始値を設定する
    setattr(obj, data_path, start_value)
    # 開始時にキーフレームを追加
    obj.keyframe_insert(data_path, frame=start_frame)

    # 中間の値を設定する
    setattr(obj, data_path, mid_value)
    # 中間地点にキーフレームを追加
    mid_frame = start_frame + (loop_length) / 2
    obj.keyframe_insert(data_path, frame=mid_frame)

    # 終了値を設定する
    setattr(obj, data_path, start_value)
    # 最終キーフレームを追加
    end_frame = start_frame + loop_length
    obj.keyframe_insert(data_path, frame=end_frame)

    if linear_extrapolation:
        set_fcurve_extrapolation_to_linear()


def set_scene_props(fps, frame_count):
    """
    シーンのプロパティを設定する
    """

    scene = bpy.context.scene
    scene.frame_end = frame_count

    # ワールドの背景を黒に設定する
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    scene.render.fps = fps

    scene.frame_current = 1
    scene.frame_start = 1


# シーンを設定する関数
def scene_setup():
    fps = 30
    loop_seconds = 12
    frame_count = fps + loop_seconds

    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()

    clean_scene()

    set_scene_props(fps, frame_count)


####################


# ジオメトリノードを接続する関数
def link_nodes_by_mesh_socket(node_tree, from_node, to_node):
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Mesh"])


def create_node(node_tree, type_name, node_x_location, node_location_step_x=0):
    """
    指定されたタイプのノードを作成し、X 軸上のノードの位置を設定、更新
    ノード オブジェクトと、次のノードの X 軸上の次の位置を返す
    """
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_x_location
    node_x_location += node_location_step_x

    return node_obj, node_x_location


def update_geo_node_tree(node_tree):
    """
    立方体メッシュ、細分化、三角化、辺分離、要素スケール
    ジオメトリノードをノードツリーに追加
    """

    out_node = node_tree.nodes["Group Output"]

    node_x_location = 0
    node_location_step_x = 300

    mesh_cube_node, node_x_location = create_node(
        node_tree, "GeometryNodeMeshCube", node_x_location, node_location_step_x
    )

    subdivide_mesh_node, node_x_location = create_node(
        node_tree, "GeometryNodeSubdivideMesh", node_x_location, node_location_step_x
    )
    subdivide_mesh_node.inputs["Level"].default_value = 3

    triangulate_node, node_x_location = create_node(
        node_tree, "GeometryNodeTriangulate", node_x_location, node_location_step_x
    )

    split_edges_node, node_x_location = create_node(
        node_tree, "GeometryNodeSplitEdges", node_x_location, node_location_step_x
    )

    scale_elements_node, node_x_location = create_node(
        node_tree, "GeometryNodeScaleElements", node_x_location, node_location_step_x
    )
    scale_elements_node.inputs["Scale"].default_value = 0.8

    out_node.location.x = node_x_location

    link_nodes_by_mesh_socket(
        node_tree, from_node=mesh_cube_node, to_node=subdivide_mesh_node
    )
    link_nodes_by_mesh_socket(
        node_tree, from_node=subdivide_mesh_node, to_node=triangulate_node
    )
    link_nodes_by_mesh_socket(
        node_tree, from_node=triangulate_node, to_node=split_edges_node
    )

    from_node = split_edges_node
    to_node = scale_elements_node
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])

    from_node = scale_elements_node
    to_node = out_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])


def create_centerpiece():
    bpy.ops.mesh.primitive_plane_add()

    bpy.ops.node.new_geometry_nodes_modifier()

    node_tree = bpy.data.node_groups["Geometry Nodes"]

    update_geo_node_tree(node_tree)

    bpy.ops.object.modifier_add(type="SOLIDIFY")


def main():
    """
    細分化し、三角化された面で構成される立方体の
    アニメーション化されたジオメトリノードを生成する
    Python コード
    """

    scene_setup()
    create_centerpiece()


if __name__ == "__main__":
    main()
