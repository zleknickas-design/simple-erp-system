from flask import Blueprint, render_template

warehouse_bp = Blueprint('warehouse', __name__, url_prefix='/warehouse')

@warehouse_bp.route('/receipts')
def receipts():
    """Warehouse receipts (incoming goods)"""
    return render_template('warehouse/receipts.html')

@warehouse_bp.route('/pickups')
def pickups():
    """Warehouse pickups (outgoing goods)"""
    return render_template('warehouse/pickups.html')

@warehouse_bp.route('/writeoffs')
def writeoffs():
    """Warehouse writeoffs (damaged/unusable goods)"""
    return render_template('warehouse/writeoffs.html')

@warehouse_bp.route('/transfers')
def transfers():
    """Warehouse transfers (between locations)"""
    return render_template('warehouse/transfers.html')
