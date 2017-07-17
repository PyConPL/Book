Agenda warsztatu
================

* Odoo - z czym to się je?
* Przygotowanie środowiska (Docker)
* Pierwsza baza i instalacja aplikacji (modułu)
* Anatomia modułu
* Model
* Widoki i menu
* Ćwiczenie 1
* Pola wyliczeniowe
* Ćwiczenie 2
* Testy

Kod z poszczególnych etapów
===========================

Minimum - przed ćwiczeniem 1
-----

`__openerp__.py`:
```python
# -*- coding: UTF-8 -*-
{
  'name': 'Rejestr piw',
  'summary': 'Obsługa rejestru piw',
  'description': '''
      Szczegółowy opis
  ''',
  'author': 'Spejson',
  'category': 'Uncategorized',
  'version': '0.0.1',
  'data': [
     'views/beer.xml'
  ]
}
```

`models/beer.py`:
```python
# -*- coding: UTF-8 -*-

from openerp import models, fields, api, _

class Beer(models.Model):
    _name = 'beer'
    _description = 'Piwo to moje paliwo'
    _log_access = True

    name = fields.Char(
        string='Nazwa',
        required=True
    )
```
`views/beer.xml`
```xml
<?xml version="1.0"?>
<openerp>
    <data>
        <record model="ir.ui.view" id="beer_tree_view">
            <field name="name">Beer list</field>
            <field name="model">beer</field>
            <field name="priority" eval="10" />
            <field name="arch" type="xml">
                <tree string="Piwunia">
                    <field name="name" />
                </tree>
            </field>
        </record>

        <record model="ir.ui.view" id="beer_form_view">
            <field name="name">Beer form</field>
            <field name="model">beer</field>
            <field name="priority" eval="10" />
            <field name="arch" type="xml">
                <form string="Piweczko" version="9.0">
                    <group string="Podstawowe">
                        <field name="name" />
                    </group>
                </form>
            </field>
        </record>

        <record model="ir.actions.act_window" id="beer_act">
            <field name="name">Piwska</field>
            <field name="res_model">beer</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
            id="beer_form_menu"
            name="Piwska"
            action="beer_act"
            sequence="200"
            />

    </data>
</openerp>
```

Uwaga! Spoilery poniżej
=======================

Przykładowe rozwiązanie ćwiczenia 1
------------------------------------

`models/beer.py`:
```python
# -*- coding: UTF-8 -*-

from openerp import models, fields, api, _

RATINGS = (
    ('1',_('słabe')),
    ('2',_('dobre')),
    ('3',_('bardzo dobre'))
)

class Beer(models.Model):
    _name = 'beer'
    _description = 'Piwo to moje paliwo'
    _log_access = True

    name = fields.Char(
        string='Nazwa',
        required=True
    )

    alc = fields.Float('% alkoholu', required=True)
    description = fields.Text('Opis')
    volume = fields.Float('Objętość [l]', required=True)
    price = fields.Float('Cena', required=True)
    rating = fields.Selection(RATINGS, string='Ocena')
```
`views/beer.xml`:
```xml
<?xml version="1.0"?>
<openerp>
    <data>
        <record model="ir.ui.view" id="beer_tree_view">
            <field name="name">Beer list</field>
            <field name="model">beer</field>
            <field name="priority" eval="10" />
            <field name="arch" type="xml">
                <tree string="Piwunia">
                    <field name="name" />
                    <field name="alc" />
                    <field name="description" />
                    <field name="volume" />
                    <field name="price" />
                    <field name="rating" />
                </tree>
            </field>
        </record>

        <record model="ir.ui.view" id="beer_form_view">
            <field name="name">Beer form</field>
            <field name="model">beer</field>
            <field name="priority" eval="10" />
            <field name="arch" type="xml">
                <form string="Piweczko" version="9.0">
                    <sheet>
                        <group string="Podstawowe" col="4">
                            <field name="name" colspan="4"/>
                            <field name="alc" />
                            <field name="volume" />
                            <field name="price" />
                            <field name="rating" />
                        </group>
                        <group string="Opis">
                            <field name="description" nolabel="1" />
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <record model="ir.actions.act_window" id="beer_act">
            <field name="name">Piwska</field>
            <field name="res_model">beer</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
            id="beer_form_menu"
            name="Piwska"
            action="beer_act"
            sequence="200"
            />

    </data>
</openerp>
```

Przykładowe rozwiązanie ćwiczenia 2
-----------------------------------
`models/beer.py`:
```python
# -*- coding: UTF-8 -*-

from openerp import models, fields, api, _

RATINGS = (
    ('1',_('słabe')),
    ('2',_('dobre')),
    ('3',_('bardzo dobre'))
)

class Beer(models.Model):
    _name = 'beer'
    _description = 'Piwo to moje paliwo'
    _log_access = True

    @api.multi
    @api.depends('alc', 'price', 'volume')
    def _calc_spejson_rating(self):
        for piwo in self:
            piwo.spejson_rating = (piwo.alc * piwo.volume / piwo.price
                if piwo.price > 0 else 999999)

    name = fields.Char(
        string='Nazwa',
        required=True
    )

    alc = fields.Float('% alkoholu', required=True)
    description = fields.Text('Opis')
    volume = fields.Float('Objętość [l]', required=True)
    price = fields.Float('Cena', required=True)
    rating = fields.Selection(RATINGS, string='Ocena')
    spejson_rating = fields.Float('Ocena Spejsona',
        compute='_calc_spejson_rating')
```

Testy
-----

`tests.py`:
```python
# -*- coding: UTF-8 -*-

from openerp.tests import common
from openerp.tools import mute_logger

class TestPiwo(common.TransactionCase):

    def test_formula(self):
        dzik_1 = self.env.ref('beer.dzik_1')
        self.assertAlmostEqual(
            dzik_1.spejson_rating,
            999999
        )
```
`demo/beer.xml`:
```xml
<?xml version="1.0"?>
<openerp><data>
    <record model="beer" id="dzik_1">
        <field name="name">Dzik</field>
        <field name="alc" eval="12.0" />
        <field name="price" eval="0" />
        <field name="volume" eval="1" />
    </record>
</data></openerp>
```
