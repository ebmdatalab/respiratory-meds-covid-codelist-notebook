# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# The following list is of products containing long acting muscarininc (LAMA) ingredients.
#
#
# - [Single Ingredient LAMAs](#single)
# - [All Multi Ingredent Preparations including LAMA](#multi)
# - [LAMA + LABA + ICS containing preparations](#triple)
# - [LAMA + LABA](#maba)

from ebmdatalab import bq
import os
import pandas as pd

# ## Single Ingredient LAMAs <a id='single'></a>

# +
sql = '''WITH bnf_codes AS (
 SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
    bnf_code LIKE '030102%'          #BNF respiratory antimusc section
    AND 
    form_route NOT LIKE '%neb%'     #exclude to nebules through name search
    AND
    (bnf_code NOT LIKE '0301020P%'  AND       #BNF oxitropium not a thing in UK
    bnf_code NOT LIKE '0301020U0%'  AND       #BNF comb product
    bnf_code NOT LIKE '0301020I0%'  )         #BNF ipratropium sama
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

lama_single_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','lama_single_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
lama_single_codelist
# -

# ## Multi Ingredent Preparations including LAMA <a id='multi'></a>

# +
sql = '''WITH bnf_codes AS (
 SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
    (bnf_code LIKE '0301020U0%'   OR        #BNF Aclidinium Brom/Formoterol
    bnf_code LIKE '0301040V0%'    OR        #BNF Aclidinium Brom/Formoterol
    bnf_code LIKE '0301040W0%'    OR        #BNF Umeclidinium bromide / Vilanterol
    bnf_code LIKE '0301040X0%'    OR        #BNF Tiotropium bromide  / Olodaterol
    bnf_code LIKE '0302000V0%A0'  OR        #BNF Fluticasone Furoate ++ 
    bnf_code LIKE '0301011AB%'    OR        #BNF Beclometasone + Formoterol + Glycopyrronium bromide
    bnf_code LIKE '0301040Y0%')          #BNF Indacaterol 85micrograms/dose / Glycopyrronium bromide
    AND 
    form_route NOT LIKE '%neb%'     #exclude to nebules through name search

  )
  
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

lama_multi_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','lama_multi_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
lama_multi_codelist

# -

# ## LAMA + LABA + ICS containing preparationss <a id='triple'></a>
#
# Recently inhalers with three ingredients have come on the market and are referred to as "triple therapy". The following is list of these preparations and have been cross checked with [NHS Rightbreathe.com](https://www.rightbreathe.com/) to ensure all BNF codes are included. 

# +
sql = '''WITH bnf_codes AS (
 SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
    (    bnf_code LIKE '0302000V0B%A0'  OR        #BNF Fluticasone + Umeclidinium bromide + Vilanterol
    bnf_code LIKE '0301011AB%')        #BNF Beclometasone + Formoterol + Glycopyrronium bromide
  #  AND 
    #form_route NOT LIKE '%neb%'     #exclude to nebules through name search

  )
  
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

resp_triple_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','resp_triple_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
resp_triple_codelist

# -

# ## LAMA + LABA <a id='maba'></a>

# +
sql = '''WITH bnf_codes AS (
 SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
    (bnf_code LIKE '0301020U0%' OR        #BNF Aclidinium Brom/Formoterol
    bnf_code LIKE '0301040V0%' OR        #BNF Aclidinium Brom/Formoterol
    bnf_code LIKE '0301040W0%'  OR        #BNF Umeclidinium bromide / Vilanterol
    bnf_code LIKE '0301040X0%'  OR        #BNF Tiotropium bromide  / Olodaterol
    bnf_code LIKE '0301040Y0%')          #BNF Indacaterol 85micrograms/dose / Glycopyrronium bromide
    AND 
    form_route NOT LIKE '%neb%'     #exclude to nebules through name search

  )
  
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

lama_laba_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','lama_laba_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
lama_laba_codelist
# -


