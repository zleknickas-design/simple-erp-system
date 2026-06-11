from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from datetime import datetime

warehouse_bp = Blueprint('warehouse', __name__, url_prefix='/warehouse')

@warehouse_bp.route('/receipts')
@login_required
def receipts():
    """Warehouse receipts (Gauvimai)"""
    return render_template('warehouse/receipts.html')

@warehouse_bp.route('/pickings')
@login_required
def pickings():
    """Warehouse pickings (Paėmimai)"""
    return render_template('warehouse/pickings.html')

@warehouse_bp.route('/write-offs')
@login_required
def write_offs():
    """Warehouse write-offs (Nurašymai)"""
    return render_template('warehouse/write_offs.html')

@warehouse_bp.route('/transfers')
@login_required
def transfers():
    """Warehouse transfers (Perkėlimai)"""
    return render_template('warehouse/transfers.html')
