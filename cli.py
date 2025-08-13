import os
import click
from divisor.config import load_config
from divisor.source import SourceFetcher
from divisor.jekyll import JekyllSite
from divisor.converter import Converter
from divisor.assets import AssetHandler
from divisor.deploy import Deployer

@click.group()
def main():
    """
    Divisor is a tool for creating Jekyll websites from Git repositories.
    """
    pass

@main.command()
@click.option("--config", default="config.yml", help="Path to the configuration file.")
def generate(config):
    """
    Generates the website.
    """
    # Load the configuration
    cfg = load_config(config)

    # Fetch the source content
    fetcher = SourceFetcher(cfg.source_repository)
    fetcher.fetch()

    # Create the Jekyll site structure
    print(f"Destination folder: {cfg.content_mapping.destination_folder}")
    site = JekyllSite(cfg.content_mapping.destination_folder, cfg)
    site.create_structure()

    # Convert the content
    converter = Converter(cfg)
    # Convert the home page
    converter.convert_file(
        f"source_repo/{cfg.content_mapping.home_page_source}",
        f"{cfg.content_mapping.destination_folder}/index.md",
        "source_repo",
    )

    # Convert the subpages
    if cfg.content_mapping.subpages_folder and cfg.content_mapping.subpages_folder != "<none>":
        subpages_source_dir = f"source_repo/{cfg.content_mapping.subpages_folder}"
        subpages_dest_dir = f"{cfg.content_mapping.destination_folder}"
        if os.path.exists(subpages_source_dir):
            for root, _, files in os.walk(subpages_source_dir):
                for file in files:
                    if file.endswith(".md"):
                        source_path = os.path.join(root, file)
                        relative_path = os.path.relpath(source_path, subpages_source_dir)
                        dest_dir = os.path.join(subpages_dest_dir, os.path.splitext(relative_path)[0])
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_path = os.path.join(dest_dir, "index.md")
                        converter.convert_file(source_path, dest_path, "source_repo")

    # Copy the assets
    asset_handler = AssetHandler(cfg)
    asset_handler.copy_assets(
        "source_repo",
        f"{cfg.content_mapping.destination_folder}/{cfg.content_mapping.media_destination_folder}",
    )

    click.echo("Website generated successfully!")

@main.command()
@click.option("--config", default="config.yml", help="Path to the configuration file.")
@click.option("--github-token", envvar="GITHUB_TOKEN", help="GitHub token for authentication.")
def deploy(config, github_token):
    """
    Deploys the website to GitHub Pages.
    """
    cfg = load_config(config)
    deployer = Deployer(cfg.content_mapping.destination_folder)
    remote_url = cfg.site_metadata.github_repository_url
    deployer.deploy(remote_url, github_token)
    click.echo("Website deployed successfully!")

@main.command()
def themes():
    """
    Lists the available Jekyll themes for GitHub Pages.
    """
    click.echo("Available themes:")
    click.echo("- architect")
    click.echo("- cayman")
    click.echo("- dinky")
    click.echo("- hacker")
    click.echo("- leap-day")
    click.echo("- merlot")
    click.echo("- midnight")
    click.echo("- minima")
    click.echo("- minimal")
    click.echo("- modernist")
    click.echo("- slate")
    click.echo("- tactile")
    click.echo("- time-machine")

@main.command()
def setup():
    """
    Interactively creates a config.yml file.
    """
    click.echo("Welcome to the Divisor setup script!")
    click.echo("This will guide you through creating your config.yml file.")

    config_data = {
        'site_metadata': {},
        'source_repository': '',
        'content_mapping': {}
    }

    # Site Metadata
    config_data['site_metadata']['title'] = click.prompt("Enter your website's title", default="My Awesome Website")
    config_data['site_metadata']['description'] = click.prompt("Enter your website's description", default="Website created with fonte.wiki and Divisor")

    available_themes = ["architect", "cayman", "dinky", "hacker", "leap-day", "merlot", "midnight", "minima", "minimal", "modernist", "slate", "tactile", "time-machine"]
    theme_prompt = "Choose a theme"
    theme_menu = "\n".join([f"{i+1}. {theme}" for i, theme in enumerate(available_themes)])
    click.echo(f"{theme_prompt}:\n{theme_menu}")

    theme_choice_index = click.prompt("Enter the number of your choice", type=click.IntRange(1, len(available_themes)), default=8)
    config_data['site_metadata']['theme'] = available_themes[theme_choice_index - 1]

    default_repo_url = "git@github.com:your-username/your-repo.git"
    config_data['site_metadata']['github_repository_url'] = click.prompt("Enter your GitHub repository URL (e.g., git@github.com:user/repo.git)", default=default_repo_url)

    repo_url = config_data['site_metadata']['github_repository_url']
    if repo_url.endswith('.git'):
        repo_name = repo_url.split('/')[-1][:-4]
        user_name = repo_url.split('/')[-2].split(':')[-1]
        default_pages_url = f"https://{user_name}.github.io/{repo_name}/"
    else:
        default_pages_url = "https://your-username.github.io/your-repo/"

    config_data['site_metadata']['github_pages_url'] = click.prompt("Enter your GitHub Pages URL", default=default_pages_url)
    config_data['site_metadata']['custom_domain'] = click.prompt("Enter your custom domain (or leave as '<none>')", default="<none>")

    # Source Repository
    config_data['source_repository'] = click.prompt("Enter the source repository URL", default="https://github.com/fonte-wiki/Backup-fonte-wiki")

    # Content Mapping
    config_data['content_mapping']['home_page_source'] = click.prompt("Enter the path to your home page file", default="home.md")
    config_data['content_mapping']['subpages_folder'] = click.prompt("Enter the folder for subpages (or '<none>')", default="<none>")
    config_data['content_mapping']['destination_folder'] = click.prompt("Enter the destination folder for the generated site", default="site_contents")
    config_data['content_mapping']['media_destination_folder'] = click.prompt("Enter the destination folder for media files", default="assets/media")

    with open("config.yml", "w") as f:
        import yaml
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

    click.echo("\nconfig.yml created successfully!")


@main.command()
def clean():
    """
    Removes the source_repo and site_contents directories.
    """
    import shutil
    if os.path.exists("source_repo"):
        shutil.rmtree("source_repo")
        click.echo("Removed source_repo directory.")
    if os.path.exists("site_contents"):
        shutil.rmtree("site_contents")
        click.echo("Removed site_contents directory.")

if __name__ == "__main__":
    main()
