import os

class JekyllSite:
    def __init__(self, path: str, config):
        self.path = path
        self.config = config

    def create_structure(self):
        """
        Creates the basic directory structure for a Jekyll website.
        """
        os.makedirs(os.path.join(self.path, "_layouts"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "_includes"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "_sass"), exist_ok=True)

        # Create Gemfile from template
        gemfile_template_path = os.path.join(os.path.dirname(__file__), "Gemfile.template")
        gemfile_path = os.path.join(self.path, "Gemfile")
        with open(gemfile_template_path, "r") as f_template:
            gemfile_content = f_template.read()

        theme_name = self.config.site_metadata.theme

        theme_gem_mapping = {
            "architect": "jekyll-theme-architect",
            "cayman": "jekyll-theme-cayman",
            "dinky": "jekyll-theme-dinky",
            "hacker": "jekyll-theme-hacker",
            "leap-day": "jekyll-theme-leap-day",
            "merlot": "jekyll-theme-merlot",
            "midnight": "jekyll-theme-midnight",
            "minima": "minima",
            "minimal": "jekyll-theme-minimal",
            "modernist": "jekyll-theme-modernist",
            "slate": "jekyll-theme-slate",
            "tactile": "jekyll-theme-tactile",
            "time-machine": "jekyll-theme-time-machine",
        }
        gem_name = theme_gem_mapping.get(theme_name, theme_name)

        gemfile_content = gemfile_content.replace('gem "minima", "~> 2.5"', f'gem "{gem_name}"')

        with open(gemfile_path, "w") as f_out:
            f_out.write(gemfile_content)

        # Create _config.yml
        config_path = os.path.join(self.path, "_config.yml")
        with open(config_path, "w") as f:
            f.write(f"title: {self.config.site_metadata.title}\n")
            f.write(f"description: {self.config.site_metadata.description}\n")
            f.write(f"theme: {gem_name}\n")
            f.write(f"url: {self.config.site_metadata.github_pages_url}\n")

        # Create CNAME file if custom_domain is set
        if self.config.site_metadata.custom_domain and self.config.site_metadata.custom_domain != "<none>":
            cname_path = os.path.join(self.path, "CNAME")
            with open(cname_path, "w") as f:
                f.write(self.config.site_metadata.custom_domain)

        # Copy layout and includes
        self.copy_template_files()

    def copy_template_files(self):
        """
        Copies the template files (_layouts, _includes, assets) to the generated site.
        """
        template_dir = os.path.dirname(__file__)
        for dir_name in ["_includes", "_layouts"]:
            # Copy default templates
            source_dir = os.path.join(template_dir, dir_name)
            dest_dir = os.path.join(self.path, dir_name)
            if os.path.exists(source_dir):
                import shutil
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)

        # Copy assets
        source_dir = os.path.join(template_dir, "assets")
        dest_dir = os.path.join(self.path, "assets")
        if os.path.exists(source_dir):
            import shutil
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            for item in os.listdir(source_dir):
                s = os.path.join(source_dir, item)
                d = os.path.join(dest_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    if item == "minima.scss" and self.config.site_metadata.theme != "minima":
                        continue
                    shutil.copy2(s, d)

            # Copy custom templates if they exist
            custom_source_dir = os.path.join("divisor", "assets")
            if os.path.exists(custom_source_dir):
                import shutil
                shutil.copytree(custom_source_dir, dest_dir, dirs_exist_ok=True)

        # Copy extended.css
        source_dir = os.path.join(template_dir, "assets")
        dest_dir = os.path.join(self.path, "assets")
        if os.path.exists(source_dir):
            import shutil
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy2(os.path.join(source_dir, "extended.css"), dest_dir)

        # Conditionally copy main.scss for minima theme
        if self.config.site_metadata.theme == "minima":
            dest_file = os.path.join(self.path, "assets", "main.scss")
            with open(dest_file, "w") as f:
                f.write("---\n")
                f.write("---\n")
                f.write('@import "minima";\n')