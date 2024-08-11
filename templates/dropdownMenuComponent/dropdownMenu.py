from .dropdownMenuInterface import DropdownMenuInterface

class DropdownMenuComponent(DropdownMenuInterface):
    def __init__(self, categories: list[str | dict]):
        self.cats = categories
        self.script = """
        <script>
            document.addEventListener('DOMContentLoaded', function () {
            
            var dropdowns = document.querySelectorAll('.dropdown-submenu');
            dropdowns.forEach(function (dropdown) {
                dropdown.addEventListener('mouseover', function () {
                this.querySelector('.dropdown-menu').classList.add('show');
                });
                dropdown.addEventListener('mouseout', function () {
                this.querySelector('.dropdown-menu').classList.remove('show');
                });
            });
            });
        </script>"""
        self.style = """
        <style>
            .dropdown-submenu {
                position: relative;
            }
            .dropdown-submenu .dropdown-menu {
                top: 0;
                left: 100%;
                margin-top: -10px;
            }
            .dropdown-menu {
                background-color: #343a40;
                color: white;
            }
            .dropdown-menu .dropdown-item {
                color: white;
            }
            .dropdown-menu .dropdown-item:hover {
                background-color: #495057;
            }
            .dropdown-submenu .dropdown-menu {
                background-color: #343a40;
            }

            .nav-item.dropdown .nav-link {
                background-color: transparent;
                color: white;
                border-radius: 0.25rem;
            }
            .nav-item.dropdown .nav-link:hover, .nav-item.dropdown .nav-link:focus, .nav-item.dropdown .nav-link:active, .nav-item.dropdown.show .nav-link {
                background-color: #343a40;
                color: white;
            }
        </style>"""

    def generate_menu(self, categories=None):
        if categories is None:
            categories = self.cats
        html = ''
        for category in categories:
            if isinstance(category, str):
                html += f'<li><a class="dropdown-item" href="#">{category}</a></li>'
            elif isinstance(category, dict):
                for key, value in category.items():
                    html += f'<li class="dropdown-submenu">'
                    html += f'<a class="dropdown-item dropdown-toggle" href="#">{key}</a>'
                    html += '<ul class="dropdown-menu">'
                    html += self.generate_menu(value)
                    html += '</ul></li>'
        return html
    
    def getStyle(self):
        return self.style
    
    def getScript(self):
        return self.script
    
    def getStyleImports(self):
        return """
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        """
    
    def getScriptImports(self):
        return """
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        """