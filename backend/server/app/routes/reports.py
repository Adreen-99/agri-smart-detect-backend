from flask import Blueprint, request, jsonify
from app import db
from app.models.report import Report
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('', methods=['GET'])
@jwt_required()
def get_reports():
    try:
        user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query user's reports
        query = Report.query.filter_by(user_id=user_id)
        
        # Filter by health status if provided
        is_healthy = request.args.get('is_healthy')
        if is_healthy is not None:
            query = query.filter(Report.is_healthy == (is_healthy.lower() == 'true'))
        
        reports = query.order_by(Report.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reports': [report.to_dict() for report in reports.items],
            'total': reports.total,
            'pages': reports.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    try:
        user_id = get_jwt_identity()
        report = Report.query.filter_by(id=report_id, user_id=user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        return jsonify({'report': report.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        user_id = get_jwt_identity()
        
        # Total scans
        total_scans = Report.query.filter_by(user_id=user_id).count()
        
        # Healthy vs diseased
        healthy_count = Report.query.filter_by(user_id=user_id, is_healthy=True).count()
        diseased_count = Report.query.filter_by(user_id=user_id, is_healthy=False).count()
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_scans = Report.query.filter(
            Report.user_id == user_id,
            Report.created_at >= week_ago
        ).count()
        
        # Most common crops
        from sqlalchemy import func
        common_crops = db.session.query(
            Report.crop_name,
            func.count(Report.id).label('count')
        ).filter(
            Report.user_id == user_id
        ).group_by(
            Report.crop_name
        ).order_by(
            func.count(Report.id).desc()
        ).limit(5).all()
        
        # Response matching frontend dashboard structure
        return jsonify({
            'total_scans': total_scans,
            'healthy_count': healthy_count,
            'diseased_count': diseased_count,
            'recent_scans': recent_scans,
            'common_crops': [{'crop': crop, 'count': count} for crop, count in common_crops],
            'health_percentage': round((healthy_count / total_scans * 100) if total_scans > 0 else 0, 1)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500