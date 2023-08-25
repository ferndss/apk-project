from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
import numpy as np

Builder.load_string('''
<CalcApp>:
	MDBoxLayout:
		orientation:"horizontal"
		MDNavigationRail:
			MDNavigationRailItem:
				text: "theme"
				icon: "theme-light-dark"
				on_press: app.callback()
			MDNavigationRailItem:
				text: "zoon in"
				icon: "magnify-plus"
				on_press: root.zoon(1)
			MDNavigationRailItem:
				text: "zoon out"
				icon: "magnify-minus"
				on_press: root.zoon(-1)
	MDBoxLayout:
		orientation: "vertical"
		#spacing: -30
		size_hint_y: 0.975
		MDTextField:
			id: dis
			hint_text: 'Distancia'		
			text: '80'
			size_hint_x: 0.6
			pos_hint: {"center_x": 0.55}
		MDTextField:
			id: pot
			hint_text: 'Potencia (CV)'
			text: '30'
			size_hint_x: 0.6
			pos_hint: {"center_x": 0.55}
		MDTextField:
			id: tns
			hint_text: 'Tensão'
			text: '380'
			size_hint_x: 0.6
			pos_hint: {"center_x": 0.55}
		MDTextField:
			id: rdm
			hint_text: 'Rendimento'
			text: '0.80'
			size_hint_x: 0.6
			pos_hint: {"center_x": 0.55}
		MDTextField:
			id: cfi
			hint_text: 'Fator de potencia'
			text: '0.80'
			size_hint_x: 0.6
			pos_hint: {"center_x": 0.55}						
		MDFloatLayout:
			#id: lbl
			#orientation: "vertical"
			#spacing: -1000
			#size_hint_y: 0.1
			MDLabel:
				id: lbl_scc
				text: ''
				color: 'blue'
				size_hint_x: 0.7
				pos_hint: {"center_x": 0.6, "y": 0.30}
			MDLabel:
				id: lbl_qdt
				text: ''
				size_hint_x: 0.7
				pos_hint: {"center_x": 0.6, "y": 0.25}
				color: 'blue'
			MDLabel:
				id: lbl_cem
				text: ''
				size_hint_x: 0.7
				pos_hint: {"center_x": 0.6, "y": 0.20}
				color: 'blue'
	FloatLayout:
		MDRoundFlatButton:
			text: 'Calcular'
			size_hint_x: 0.4
			pos_hint: {"y": 0.1, "center_x":0.5}
			on_press: root.function()
''')

class CalcApp(MDFloatLayout):
	def zoon(self, op):
		if self.ids.lbl_scc.font_size < (68-op) and self.ids.lbl_scc.font_size > 46-op:
			self.ids.lbl_scc.font_size += 1*op
			
		if self.ids.lbl_qdt.font_size < 70-op and self.ids.lbl_qdt.font_size > 46-op:
			self.ids.lbl_qdt.font_size += 1*op#str(i)
			self.ids.lbl_qdt.pos_hint = {"y": self.ids.lbl_qdt.pos_hint["y"] - 0.001*op}
			
		if self.ids.lbl_cem.font_size < 55-op and self.ids.lbl_cem.font_size > 46-op:
			self.ids.lbl_cem.font_size += 1*op#str(i)
			self.ids.lbl_cem.pos_hint = {"y": self.ids.lbl_cem.pos_hint["y"] - 0.005*op}
		
	def function(self):
		dis = float(self.ids.dis.text)
		pot = float(self.ids.pot.text)
		tns = float(self.ids.tns.text)
		rdm = float(self.ids.rdm.text)
		cfi = float(self.ids.cfi.text)
		cb = cable_calc(dis, pot, tns, rdm, 0.0172,
											cfi, pl=4)
													
		self.ids.lbl_scc.text = "seção do cabo: {} mm".format(cb.cable_sec())
		self.ids.lbl_qdt.text = "queda de tensão: {} %".format(round(cb.voltage_drop(),2))
		self.ids.lbl_cem.text = "corrente eletrica 40°C: {} A".format(round(cb.temp(),2))

class MyApp(MDApp):
	def build(self):
			return CalcApp()
	def callback(self):
			self.theme_cls.theme_style = ("Dark" if self.theme_cls.theme_style == "Light" else "Light")
	
		
class cable_calc:	
	def __init__(self, L, P, V, rd, ro, fi, 
							fq=60, fs=1, pl=None):
		self.L = L
		self.P = P*735.5
		self.V = V
		self.fi = fi
		self.ro = ro
		self.rd = rd
		self.fq = fq
		self.fs = fs
		self.pl = pl
	
	def cable_sec(self):	
		Ss = np.array([1.5, 2.5, 4, 6, 
									10, 16, 25, 35, 
									50, 70, 95, 120])
		S = (self.temp()*self.L*2*self.ro*np.sqrt(3))/(0.05*self.V)
		return [i for i in Ss if i >= S][0]
	def rpm(self):
		return 120*self.fq/self.pl		
	def amp(self):
		return (self.P*self.fs)/(self.V*np.sqrt(3)*self.fi*self.rd)		
	def cable_res(self):
		return self.ro*self.L/self.cable_sec()		
	def voltage_drop(self):
			return 100*(3*self.cable_res()*self.temp()*self.fi)/(self.V)
	def temp(self):
		return (self.amp()/0.91)
		
if __name__ == "__main__":
	MyApp().run()