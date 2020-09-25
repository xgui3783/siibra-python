#!/usr/bin/env python3
import click
from brainscapes import logger, parcellations, spaces, atlases, features as features_
from brainscapes.termplot import FontStyles as style

# ---- Autocompletion functions ----

def complete_parcellations(ctx, args, incomplete):
    """ auto completion for parcellations """
    return [p for p in dir(parcellations) 
            if p.startswith(incomplete)]

def complete_regions(ctx, args, incomplete):
    """ auto completion for parcellations """
    atlas = atlases[0]
    for option in ['-p','--parcellation']:
        if args.count(option):
            pname = args[args.index(option)+1]
            atlas.select_parcellation(pname)
    regions = [c.key 
            for r in atlas.regiontree.iterate()
            for c in r.children ]
    search = [r for r in regions if incomplete.upper() in r]
    return search if len(search)>0 else ""

def complete_spaces(ctx, args, incomplete):
    """ auto completion for parcellations """ 
    return [s for s in dir(spaces) 
            if s.startswith(incomplete)]

def complete_genes(ctx, args, incomplete):
    """ autocompletion for genes """
    if len(incomplete)>0:
        return [a for a in features_.gene_names.keys() 
                if a.startswith(incomplete)]
    else:
        return ""

def complete_regional_modalities(ctx, args, incomplete):
    """ auto completion for regional feature types """
    return [m for m in features_.modalities
            if m.startswith(incomplete) 
            and features_.feature.GlobalFeature 
            not in features_.classes[m].__bases__ ] + ['RegionProps']

def complete_global_modalities(ctx, args, incomplete):
    """ auto completion for global feature types """
    return [m for m in features_.modalities
            if m.startswith(incomplete) 
            and features_.feature.GlobalFeature 
            in features_.classes[m].__bases__ ]

# ---- Main command ----

@click.group()
@click.option('-p','--parcellation', type=click.STRING, default=None, 
        autocompletion=complete_parcellations,
        help="Specify another than the default parcellation")
@click.option('-s','--space',  type=click.STRING, default=None,
        autocompletion=complete_spaces,
        help="Specify a template space")
@click.pass_context
def brainscapes(ctx,parcellation,space):
    """ Command line interface to the brainscapes atlas services.
    """
    ctx.obj = {}
    ctx.obj['atlas'] = atlas = atlases[0]

    if parcellation is not None:
        try:
            atlas.select_parcellation(parcellation)
        except Exception as e:
            print(str(e))
            logger.error("No such parcellation available: "+parcellation)
            exit(1)
    logger.info('Selected parcellation "{}"'.format(
        ctx.obj['atlas'].selected_parcellation.name))

    if space is None:
        ctx.obj['space'] = atlas.spaces[0]
    else:
        if spaces.obj(space) in atlas.spaces:
            ctx.obj['space'] = spaces.obj(space)
        else:
            logger.error("Space {} is not supported by atlas {}.".format(
                    atlas,space))
            exit(1)
    logger.info('Using template space "{}"'.format(ctx.obj['space']))

# ---- Commands for working with the region hierarchy ----

@brainscapes.group()
@click.pass_context
def regions(ctx):
    """
    Work with the region hierarchy of the selected parcellation.
    """
    pass

@regions.command()
@click.argument('searchstring', type=click.STRING)
@click.option('-i','--case-insensitive',is_flag=True,
        help="Ignore case when searching")
@click.pass_context
def search(ctx,searchstring,case_insensitive):
    """
    Search regions by name.
    """
    atlas = ctx.obj['atlas']
    matches = atlas.regiontree.find(searchstring,exact=False)
    for m in matches:
        print(m.name)

@regions.command()
@click.pass_context
def tree(ctx):
    """
    Print the complete region hierarchy as a tree.
    """
    atlas = ctx.obj['atlas']
    print(atlas.regiontree)

# ---- Commands for retrieving data features ---

@brainscapes.command()
@click.argument('modality', type=click.STRING, 
        autocompletion=complete_regional_modalities)
@click.argument('region', type=click.STRING,
        autocompletion=complete_regions )
@click.option('-g','--gene', type=click.STRING, default=None,
        autocompletion=complete_genes )
@click.pass_context
def features(ctx,modality,region,gene):
    """
    Retrieve region specific data features.
    """
    atlas = ctx.obj['atlas']
    atlas.select_region(region)
    print(atlas.selected_region)

    if modality=='RegionProps':
        space = ctx.obj['space']
        results = [atlas.regionprops(space)]
        print(style.BOLD+"Region properties"+style.END)
    elif modality=='GeneExpression':
        if gene is None:
            print("You need to specify a gene with the -g option when looking up gene expressions.")
            return 1
        results = atlas.query_data(modality,gene=gene)
        print(style.BOLD+"Gene Expressions"+style.END)
    else:
        results = atlas.query_data(modality)
        print(style.BOLD+"{} features".format(modality)+style.END)

    print(style.END)
    for result in results:
        print(result)

@brainscapes.command()
@click.argument('modality', type=click.STRING, 
        autocompletion=complete_global_modalities)
@click.pass_context
def globals(ctx,modality):
    """
    Retrieve global data features.
    """
    atlas = ctx.obj['atlas']
    features = atlas.query_data(modality)
    for feature in features:
        print(feature)

