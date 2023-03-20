{
    "name": "Gestion des étudiants",
    "version": "0.1",
    "category": "Generic Modules/Others",
    "description": """Test création module gestion des étudiants Odoo v14""",
    "author": "Moi",
    "depends": ["base"],
    "data": [
        "data/students_training_data.xml",
        "data/students_student_data.xml",
        "views/students_views.xml",
        "views/res_partner_views.xml"
    ],
    "installable": True,
    "auto_install": False,
}
