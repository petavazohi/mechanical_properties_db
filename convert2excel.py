#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:28:36 2020

@author: petavazohi
"""

import json
import mechelastic
import pandas as pd

df = pd.DataFrame(columns=['Material id',
                                    'Formula',
                                    'Space Group',
                                    'Crystal System',
                                    'nsites',
                                    'Bulk(vrh)',
                                    'Shear(vrh)',
                                    'Young(vrh)',
                                    'Poisson(vrh)']) 
                

rf = open('MaterialsProject_Elastic.json','r')
data = json.load(rf)
rf.close()
i = 1
for idata in data:
    
    elastic_tensor    = idata['elasticity']['elastic_tensor']
    compliance_tensor = idata['elasticity']['compliance_tensor']
    formula = idata['pretty_formula']
    material_id = idata['material_id']
    spg = idata['spacegroup']['number']
    crystal_system = idata['spacegroup']['crystal_system']
    nsites = idata['elasticity']['nsites']
    try:
        elastic_properties = mechelastic.ElasticProperties(elastic_tensor=elastic_tensor)
        bulk = elastic_properties.bulk_modulus_voigt_reuss_hill
        shear = elastic_properties.shear_modulus_voight_reuss_hill
        young = elastic_properties.youngs_modulus_voigt_reuss_hill
        poisson = elastic_properties.poissons_ratio_voigt_reuss_hill
    except :
        bulk = None
        shear = None
        young = None
        poisson = None
    
    temp_dict = {'Material id':material_id,
                 'Formula':formula,
                 'Space Group':spg,
                 'Crystal System':crystal_system,
                 'nsites':nsites,
                 'Bulk(vrh)':bulk,
                 'Shear(vrh)':shear,
                 'Young(vrh)':young,
                 'Poisson(vrh)':poisson}
    df = df.append(pd.DataFrame(temp_dict,index=[i]),ignore_index=True)
    print(material_id,formula)
    i+=1

with pd.ExcelWriter('MaterialsProject_Elastic.xlsx') as writer:
    df.to_excel(writer,sheet_name='Sheet1')
