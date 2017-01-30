import os
import random
import click
import silly
from flask.cli import with_appcontext
from .. import app, db
from ..main import user_datastore
from ..core.models import Site
from ..page.models import Page
from ..blog.models import Post, Tag, Category
from ..user.models import Profile, Role

babel_options = app.config['BABEL']

@app.cli.command('createdb')
def create_db():
    if os.path.exists(app.config['DB_DIR']):
        click.echo("Found an existing database")
        click.echo("Destroying old database")
        os.remove(app.config['DB_DIR'])
    click.echo("Creating new database")
    db.create_all()
    print("Adding a new Site...")
    s = Site(
      name="Singularity Website",
      is_active=True
    )
    click.echo("Adding admin user")
    admin_role = Role(name="admin")
    db.session.add(admin_role)
    user = user_datastore.create_user(
        user_name='admin',
        email='admin@localhost',
        password='admin',
        roles=[admin_role])
    profile = Profile(first_name='Canella', last_name='User', user=user)
    db.session.add(profile)
    db.session.add(s)
    click.echo("Adding blog page")
    db.session.add(Page(title="Blog", content="<p>Blog</p>"))
    db.session.add(Page(title="Home", content="<h1>Home</h1>", slug='index'))
    click.echo("adding default category")
    db.session.add(Category(title="Uncategorized"))
    click.echo("Adding posts")
    cats = [Category(title=t) for t in ['Life', 'Programming', 'Accessibility', 'Music', 'Books']]
    tags = [Tag(title=t) for t in ['Python', 'Flask', 'Open-Source', 'H2G2', 'Armik', 'Aria']]
    for i, post in enumerate([Post(title=t) for t in ['Who is Me?', 'Aria and HTML Standards', 'Mostly Harmless', 'Lost In Guitar', 'An Anatomy of The Life']]):
        post.category = cats[i]
        post.body = '<p>'.join([silly.paragraph() for i in range(20)])
        post.status = 'published'
        post.tags.update(set([random.choice(tags) for i in range(5)]))
        db.session.add(post)
    db.session.commit()
    click.echo("Process Completed!")

def run_system_command(command, success, failure='Oparation faild, check the error log above'):
    exit_code = os.system(command)
    click.echo(success if exit_code==0 else failure)

@app.cli.group()
def babel():
    """Internationalization related utilities"""


@babel.command('pot')
@click.option('--output',  default=babel_options['catalog_filename'], help='Output file name', prompt="Output directory")
@click.option('--project', default=babel_options['project_name'], help='Name of the project', prompt="Project Name:")
@click.option('--target', default=app.root_path, help='Project directory', prompt="project directory")
@click.option('--config', default=babel_options['babel_config'], prompt="Babel config file")
def generate_translation_catalog(output, project, target, config):
    """Generates translation catalog for this app"""
    target, config, output = [os.path.abspath(p) for p in (target, config, output)]
    cmd = 'pybabel extract -F "{config}" -k gettext -k ngettext -k _trans -k _ntrans -k lazy_gettext -o "{output}" --project "{project}" "{target}"'.format(output=output, project=project, target=target, config=config)
    run_system_command(
        cmd,
        success='Successfully generated translation catalog, find it at: %s' %output,
    )

@babel.command('mo')
@click.option('--domain', default=babel_options['domain'], prompt='Translation Domain:')
@click.option('--target', default=babel_options['translations_directory'], prompt='Translation Directory:')
def compile_catalog(domain, target):
    """Compiles the translations"""
    target = os.path.abspath(target) 
    cmd = 'pybabel compile -f -D {domain} -d "{target}"'.format(domain=domain, target=target)
    run_system_command(
        cmd,
        success='messages were compiled successfully',
    )

@babel.command('new')
@click.option('--language-code', prompt='Language Code:', required=True)
@click.option('--catalog', default=babel_options['catalog_filename'], prompt='Translation Catalog:')
@click.option('--target', default=babel_options['translations_directory'], prompt='Translation Directory:')
@click.option('--domain', default=babel_options['domain'], prompt='Translation Domain:')
def add_new_language(language_code, catalog, target, domain):
    """Adds a new translation"""
    if language_code not in [code for code, label in app.config['SUPPORTED_LANGUAGES']]:
        return click.echo('The supplied language code is not in the SUPPORTED_LANGUAGES setting. Please add it first.')
    target, catalog = [os.path.abspath(p) for p in (target, catalog)]
    cmd = 'pybabel init -i "{catalog}" -D {domain} -d "{target}" -l {language_code}'.format(catalog=catalog, language_code=language_code, target=target, domain=domain)
    run_system_command(
        cmd,
        success='Language messages were added  to %s' %target,
    )

@babel.command('update')
@click.option('--catalog', default=babel_options['catalog_filename'], prompt='Translation Catalog:')
@click.option('--target', default=babel_options['translations_directory'], prompt='Translations Directory:')
@click.option('--domain', default=babel_options['domain'], prompt='Translation Domain:')
def update_from_pot(catalog, target, domain):
    """Updates messages from POT file"""
    target, catalog = [os.path.abspath(p) for p in (target, catalog)]
    cmd = 'pybabel update -i "{catalog}" -D {domain} -d "{target}"'.format(catalog=catalog, target=target, domain=domain)
    run_system_command(
        cmd,
        success='messages were updated from POT file',
    )
    