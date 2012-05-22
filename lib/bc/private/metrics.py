#!/usr/bin/python2.6
import bobject
import readonly

from bc import database

class TariffRateConstants(object):
	__metaclass__ = readonly.metaClass
	__readonly__  = {
		'FORMULA_SPEED': 'speed',
		'FORMULA_TIME':  'time',
		'FORMULA_UNIT':  'unit',
	}

constants = TariffRateConstants()

class Metric(bobject.BaseObject):
	def __init__(self, data = None):
		self.__values__ = {
			'id':         '',
			'type':       '',
			'formula':    '',
			'aggregate':  0,
		}

		if data:
			self.set(data)


def add(metric):
	"""Creates new billing metric"""

	with database.DBConnect() as db:
		db.insert('metrics', metric.values)


def get_all():

	with database.DBConnect() as db:
		for i in db.query("SELECT * FROM `metrics` m;"):
			yield Metric(i)

