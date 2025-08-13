# Divisor (de águas)

Divisor is a Python-based tool that automates the creation of a Jekyll-powered website from an existing Git repository that keeps a backup of a wiki.js powered website.

The core idea is to provide a simple and flexible way to generate a static website from selected contents, without having to manually set up a Jekyll environment or manage the content conversion process manually. The resulting website will be deployed to GitHub Pages by default.

## How it works

The first basic step is to fetch the contents from the source repository. Then, the tool will generate a Jekyll website based on the configuration file `config.yml`. The generated website will be placed in the `destination_folder` defined in the configuration file.

The `config.yml` file allows you to customize the generated website. You can define the site's title, description, theme, and other options. You can also map specific files and folders from your source repository to the generated website.

## Configuration

The main configuration file is `config.yml`. Here's a breakdown of the available options:

```yaml
site_metadata:
  title: "My Awesome Website"
  description: "Website created with fonte.wiki and Divisor"
  theme: "minima"

  github_repository_url: "https://github.com/your-git-username/your-repository.git" # Recommended: use HTTPS URL

  github_pages_url: "https://your-git-username.github.io/your-repository/" #edit this line

  custom_domain: "<none>" # Add your custom domain here, or leave as '<none>'

source_repository: "https://github.com/fonte-wiki/Backup-fonte-wiki" #leave this to use fonte.wiki as the source repository

content_mapping:
  home_page_source: "home.md" #edit this line to choose the home page of your website
  subpages_folder: "<none>" #optionally add a folder from the source repository whose contents will be imported as subpages
  destination_folder: "site_contents"
  media_destination_folder: "assets/media"
```

### `site_metadata`

*   `title`: The title of your website.
*   `description`: A short description of your website.
*   `theme`: The Jekyll theme to use. Defaults to "minima". For a list of available themes, run `python cli.py themes`.
*   `github_repository_url`: The address of your repository.
*   `github_pages_url`: The URL of your GitHub Pages website.
*   `custom_domain`: The custom domain to use for your website. If you're not using a custom domain, leave this as `<none>`. When a custom domain is provided, a `CNAME` file will be automatically generated.

### `source_repository`

The URL of the Git repository to use as the source for your website's content.

### `content_mapping`

*   `home_page_source`: The path to the Markdown file to use as the home page.
*   `subpages_folder`: The path to the folder containing the subpages. To disable subpages, set this field to `<none>`.
*   `destination_folder`: The folder where the generated Jekyll site will be created.
*   `media_destination_folder`: The folder where the media files will be copied.

## Getting Started

There are two ways to use Divisor to generate and deploy your website:

### Interactive Setup (Recommended)

The easiest way to get started is to use the interactive setup script. This will guide you through the process of creating your `config.yml` file.

```bash
python cli.py setup
```

This command will ask you a series of questions about your website and generate a `config.yml` file based on your answers.

### Manual Setup

This option is ideal if you want to generate a one-time static website from the current state of your source repository.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/fonte-wiki/divisor.git
    cd divisor
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure the website:**
    You can either create a `config.yml` file manually (by renaming `config.yml.sample`) or use the interactive setup script:
    ```bash
    python cli.py setup
    ```
4.  **Generate the website:**
    ```bash
    python cli.py generate
    ```
    **Note:** This command will always fetch the latest content from the source repository before generating the website.
5.  **Preview the website locally (Requires Ruby/Jekyll):**
    To preview your site locally, you'll need to have Ruby and Bundler installed. Then, `cd` into your generated site's directory and run:
    ```bash
    bundle install
    bundle exec jekyll serve
    ```
6.  **Deploy the website (Manual Only):**
    To deploy the website to GitHub Pages, run:
    ```bash
    python cli.py deploy
    ```
    **Note:** This command is intended for manual deployments only. If you are using the automated GitHub Actions setup, you do not need to run this command.
    The destination repository is configured in the `config.yml` file via the `github_repository_url` field.
7.  **GitHub Pages Setup:**
    If you manually deploy your generated Jekyll source files to a gh-pages branch, you need to configure GitHub Pages:
    * **Ensure `gh-pages` branch exists:**
    If it doesn't, create it:
    ```bash
    git checkout --orphan gh-pages
    git rm -rf . # Remove all files from the new orphan branch
    git commit --allow-empty -m "Initial gh-pages commit"
    git push origin gh-pages
    git checkout main # Go back to your main branch
    ```

    * **Configure GitHub Pages:**
    In your GitHub repository's `Settings > Pages` section:
        * Set "Source" to "Deploy from a branch".
        * Select the `gh-pages` branch and / (root) folder.
        * Click "Save".

### Option B: Automated Setup with GitHub Actions

This option provides a fully automated way to keep your website in sync with your source repository.

1.  **Fork Divisor to your GitHub account:**
    Fork this repository (`https://github.com/fonte-wiki/divisor`) to your own GitHub account or organization.
2.  **Enable workflows in your forked repository:**
    By default, GitHub Actions workflows are disabled on forked repositories. To enable them, go to the "Actions" tab in your forked repository and click the "I understand my workflows, go ahead and enable them" button.
3. **Rename Workflow Files:**
    The workflow files are provided with a .sample extension to prevent them from running automatically in the main Divisor repository. For automated deployment in your forked repository, you need to rename them:
    * Rename `.github/workflows/generate-website.yml-sample` to `.github/workflows/generate-website.yml`
    * Rename `.github/workflows/deploy-website.yml-sample` to `.github/workflows/deploy-website.yml`
    You can do this directly on GitHub's web interface or by cloning the repository, renaming locally, and pushing the changes.
4.  **Configure GitHub Pages settings:**
    Before your first deployment, ensure your GitHub Pages are set up:
    * Navigate to your forked repository on GitHub.
    * Go to `Settings > Pages`.
    * Under "Build and deployment", ensure:
        * "Source" is set to "Deploy from a branch".
        * "Branch" is set to `gh-pages` and `/ (root)`.
    * Click "Save".
    (GitHub will automatically create the gh-pages branch on the first successful push by the deployment action.)
5. **Set up GitHub Secrets:**
    The automated workflow uses a Personal Access Token (PAT) to authenticate and push the generated Jekyll site to your `gh-pages` branch. You need to create this PAT and add it as a repository secret.
    * **Generate a Personal Access Token (PAT):**
        * Go to your GitHub profile settings: `Settings > Developer settings > Personal access tokens > Tokens (classic)`.
        * Click "Generate new token (classic)".
        * **Note:** Give it a descriptive name (e.g., `Divisor GH Pages Deploy Token`).
        * **Expiration:** Set an appropriate expiration (e.g., 90 days, 1 year, or "No expiration" for continuous deployment, though regular rotation is good practice).
        * **Select Scopes:** Crucially, enable the `repo` scope. This grants the token sufficient permissions to push content to your `gh-pages` branch.
        * Click "Generate token" and **immediately copy the token value**. You will not see it again.
    * **Add the PAT as a Repository Secret:**
        * Navigate to your forked Divisor repository on GitHub.
        * Go to `Settings > Secrets and variables > Actions`.
        * Click "New repository secret".
        * **Name:** Enter `GH_PAGES_TOKEN` (this name must match exactly what is used in the `deploy-website.yml` workflow).
        * **Value:** Paste the PAT you copied in the previous step.
        * Click "Add secret".
6.  **Configure Divisor's `config.yml`:**
    * You can either create a `config.yml` file manually (by renaming `config.yml.sample`) or use the interactive setup script:
      ```bash
      python cli.py setup
      ```
    * Edit the `config.yml` file to customize your website.
    * Crucially, ensure `site_metadata.github_pages_url` is set correctly for your forked repository's GitHub Pages URL. For example, if your forked repo is `your-username/divisor`, github_pages_url should be `https://your-username.github.io/divisor/`.
    * The baseurl generated by Divisor in `_config.yml` (within `site_contents`) will be derived from this, and it must match your GitHub Pages path (e.g., `/divisor`).
7.  **Workflow Files Setup:**
    The necessary GitHub Actions workflow files are already included in the `.github/workflows/` directory of this repository, but require renaming as described in step 3.
8.  **Commit and push:**
    Commit your `config.yml` changes (and the renamed workflow files from step 3) to your forked repository. A `push` event will automatically trigger the `generate-website.yml` workflow, which, upon completion, will trigger the `deploy-website.yml` workflow.


## Automated Workflow Details

This repository includes two GitHub Actions workflows that automate the process of generating and deploying the website:

1.  `generate-website.yml`:
    * **Triggers:** Runs automatically every hour (`cron: '0 * * * *'`), can be triggered manually via `workflow_dispatch`, or on every `push` to the repository.
    * **Steps:** Checks out the repository, sets up the Python environment, installs dependencies, runs `python cli.py generate` to fetch content and create the Jekyll source files in `site_contents`. It then uploads these generated files as a GitHub Action artifact named `jekyll-site-source`.
2.  `deploy-website.yml`:
    * **Triggers:** Activated automatically (`workflow_run`) once the `generate-website.yml` workflow successfully completes.
    * **Steps:** Checks out the repository, downloads the `jekyll-site-source `artifact from the completed `generate-website.yml` run. It then uses the `peaceiris/actions-gh-pages` action to push the Jekyll source to your `gh-pages` branch. Crucially, the `disable_nojekyll: true` option is used to ensure GitHub Pages processes your content as a Jekyll site (rather than serving it as plain static files).

## Choosing a Theme

Divisor supports all Jekyll themes that are compatible with GitHub Pages. To see a list of available themes, run the following command:

```bash
python cli.py themes
```

This will output a list of themes that you can use in your `config.yml` file.

To change the theme of your website, simply update the `theme` field in your `config.yml` file with the name of the desired theme. For example:

```yaml
site_metadata:
  title: "My Awesome Website"
  description: "Website created with fonte.wiki and Divisor"
  theme: "cayman" # Changed from "minima"
  # ...
```

After changing the theme, commit the changes to your `config.yml` file. If you are using the automated setup, the GitHub Actions workflow will automatically regenerate and deploy your website with the new theme.

## Custom Templates and Layouts

You can customize the look and feel of your site by providing your own templates and layouts. To do so, create `_layouts` and `_includes` directories inside the `divisor` directory:

*   `divisor/_layouts`: Place your custom layouts in this directory.
*   `divisor/_includes`: Place your custom includes in this directory.

When you run the `generate` command, Divisor will copy the contents of these directories to the generated site, overwriting any default files with the same name. This allows you to either add new templates or override the default ones provided by the theme.

### Customizing the CSS

To add your own custom CSS, you can create a file named `extended.css` in the `divisor/assets` directory. This file will be loaded after the theme's default CSS, allowing you to override any styles you want. This is the recommended way to add custom styles for any theme.

## `setup.py`

The `setup.py` file is a standard Python script that's used to package and distribute the Divisor tool. It defines the package name, version, dependencies, and entry points. You don't need to interact with this file directly unless you want to modify the packaging of the tool.
