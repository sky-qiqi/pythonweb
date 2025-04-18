from flask import Blueprint, request, jsonify
from recommendation.collaborative_filtering import recommend_movies_for_user
from models import User

# 创建蓝图
main_bp = Blueprint('main', __name__)

@main_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """获取指定用户的电影推荐."""
    # 检查用户是否存在 (可选)
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': f'User with id {user_id} not found'}), 404

    # 获取推荐数量，默认为 10
    num_recommendations = request.args.get('count', 10, type=int)

    try:
        # 调用协同过滤推荐函数
        recommendations = recommend_movies_for_user(user_id, num_recommendations)

        if not recommendations:
            return jsonify({'message': f'No recommendations available for user {user_id}'}), 200

        return jsonify(recommendations)

    except Exception as e:
        # 记录错误日志会更好
        print(f"Error generating recommendations for user {user_id}: {e}")
        return jsonify({'error': 'An internal error occurred while generating recommendations.'}), 500

# 可以在这里添加其他 API 端点，例如：
# - 获取电影详情
# - 获取用户信息
# - 添加/更新评分
# - 基于内容的推荐端点
# - 混合推荐端点