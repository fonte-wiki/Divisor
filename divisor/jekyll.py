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
            f.write(f"about_page_title: {self.config.site_metadata.about_page_title}\n")

        # Copy layout and includes
        self.copy_template_files()

        # Create about page
        self.create_about_page()

    def create_about_page(self):
        """
        Creates the about page from the config.
        """
        about_path = os.path.join(self.path, "about.md")
        with open(about_path, "w") as f:
            f.write("---\n")
            f.write("layout: page\n")
            f.write(f"title: {self.config.site_metadata.about_page_title}\n")
            f.write("---\n")
            f.write(f"\n{self.config.site_metadata.about_page_body}\n")

    def copy_template_files(self):
        """
        Copies the template files (_layouts, _includes, assets) to the generated site.
        """
        template_dir = os.path.dirname(__file__)
        for dir_name in ["_includes", "_layouts"]:
            source_dir = os.path.join(template_dir, dir_name)
            dest_dir = os.path.join(self.path, dir_name)
            if os.path.exists(source_dir):
                import shutil
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir)
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
