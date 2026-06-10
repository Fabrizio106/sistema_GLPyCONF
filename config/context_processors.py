def menu_context(request):
    route_name = request.resolver_match.url_name if request.resolver_match else ""

    menu_map = {
        # GLP
        "registrar_glp": {
            "module_title": "GLP",
            "module_icon": "bi-fuel-pump",
            "page_title": "Nuevo certificado",
        },
        "historial_glp": {
            "module_title": "GLP",
            "module_icon": "bi-fuel-pump",
            "page_title": "Historial",
        },

        # Administración
        "gestion_sedes": {
            "module_title": "Administración",
            "module_icon": "bi-gear",
            "page_title": "Sedes",
        },
        "gestion_usuarios": {
            "module_title": "Administración",
            "module_icon": "bi-gear",
            "page_title": "Usuarios",
        },

        # Conformidades
        "conformidad_form": {
            "module_title": "Conformidades",
            "module_icon": "bi-list-check",
            "page_title": "Nueva conformidad",
        },
        "historial_conformidades": {
            "module_title": "Conformidades",
            "module_icon": "bi-list-check",
            "page_title": "Historial",
        },

        # Reportes
        "reporte_glp_admin": {
            "module_title": "Reportes",
            "module_icon": "bi-bar-chart-line",
            "page_title": "Reporte GLP",
        },
    }

    return menu_map.get(route_name, {
        "module_title": "Sistema",
        "module_icon": "bi-grid",
        "page_title": "Panel principal",
    })