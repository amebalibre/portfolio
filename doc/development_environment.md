# Preparing Development Environment


1.  Download a IDE: [Atom](https://atom.io/)

2.  Install pip, check next [documentation](https://pip.pypa.io/en/stable/installing/)
    1.  (OPTIONAL) If you download and install **Atom**, you should install this dependencies:
         ```bash
         pip install elpy jedi flake8 importmagic autopep8 yapf epc
        ```
    2.  (OPTIONAL) If you download and install **Atom**, you should install this packages:
        *   autocomplete-python
        *   build
        *   django-templates
        *   editorconfig
        *   emmet
        *   file-icons
        *   jumpy
        *   linter
        *   linter-flake8
        *   linter-markdown
        *   minimap

3.  Install virtualenv:
     ```bash
     apt install virtualenv
     ```

4.  Create a Projects dir, for example:
     ```bash
     mkdir -p ~/Proyectos/django
     ```

5.  Download repository
     ```bash
     cd ~/Proyectos/django
     git clone git@github.com:amebalibre/portfolio.git
     ```

6.  Create a virtual environment:
     ```bash
     virtualenv .env
     ```

7.  Active virtual environment and install dependencies:
     ```bash
     source .env/bin/activate
     pip install django
    ```
