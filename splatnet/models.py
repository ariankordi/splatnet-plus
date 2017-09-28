from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from PIL import Image
from base64 import b64encode
from io import BytesIO

# Create your models here.

class Base64ImageField(models.TextField):
    pass

class Player(models.Model):
	# Player stats
	PId = models.IntegerField(primary_key=True)
	MiiName = models.CharField(max_length=32, blank=True)
	Region = models.CharField(max_length=2, blank=True, null=True)
	Area = models.IntegerField(default=0)
	
	# REMOTE_ADDR for the purpose of, well, I don't know
	#RemoteAddr = models.GenericIPAddressField(null=True)
	
	CreatedTime = models.DateTimeField(auto_now_add=True)
	LatestTime = models.DateTimeField(auto_now=True)
	
	# Game player stats
	Model = models.SmallIntegerField(default=0, choices=((0, 'Girl'), (1, 'Boy'), (2, 'Octoling')))
	Skin = models.SmallIntegerField(default=0, choices=((0, '1'), (1, '2'), (2, '3'), (3, '4'), (4, '5'), (5, '6'), (6, '7'), (7, 'Unknown'), (8, 'Unknown')))
	EyeColor = models.SmallIntegerField(default=0, choices=((0, 'Brown'), (1, 'Pink'), (2, 'Blue'), (3, 'Orange'), (4, 'Green'), (5, 'Black'), (6, 'Yellow'), (7, 'Unknown'), (8, 'Unknown')))
	
	# Weapon/gear stats
	CurrentWeapon = models.IntegerField(default=0)
	Gear_Shoes = models.IntegerField(default=0)
	Gear_Shoes_Skill0 = models.IntegerField(default=0)
	Gear_Shoes_Skill1 = models.IntegerField(default=0)
	Gear_Shoes_Skill2 = models.IntegerField(default=0)
	Gear_Clothes = models.IntegerField(default=0)
	Gear_Clothes_Skill0 = models.IntegerField(default=0)
	Gear_Clothes_Skill1 = models.IntegerField(default=0)
	Gear_Clothes_Skill2 = models.IntegerField(default=0)
	Gear_Head = models.IntegerField(default=0)
	Gear_Head_Skill0 = models.IntegerField(default=0)
	Gear_Head_Skill1 = models.IntegerField(default=0)
	Gear_Head_Skill2 = models.IntegerField(default=0)

	# Level/Rankings (Rank is level, Udemae is rank)
	Rank = models.SmallIntegerField(default=0, validators=[MaxValueValidator(49), MinValueValidator(0)])
	Udemae = models.SmallIntegerField(default=0, choices=((0, 'C-'), (1, 'C'), (2, 'C+'), (3, 'B-'), (4, 'B'), (5, 'B+'), (6, 'A-'), (7, 'A'), (8, 'A+'), (9, 'S'), (10, 'S+')))
	RegularKillSum = models.BigIntegerField(default=0)
	WinSum = models.BigIntegerField(default=0)
	LoseSum = models.BigIntegerField(default=0)
	Money = models.BigIntegerField(default=0)
	Shell = models.BigIntegerField(default=0)
	
	Face = Base64ImageField(blank=True)

	def __str__(self):
		return str(self.PId) + ' ('+ self.MiiName +'), a player last connected at ' + str(self.LatestTime)

	def get_face_from_request(self, request):
		if request.FILES.get('FaceImg'):
			face_file = request.FILES['FaceImg']
			im = Image.open(face_file)
			imbg = im.convert()
			imfile = BytesIO()
			imbg.save(imfile, quality=100, format='PNG')
			self.Face = 'data:image/png;base64,' + b64encode(imfile.getvalue()).decode()
		else:
			self.Face = ''
	
	def get_Rank_display(self):
		return str(self.Rank + 1)
class Session(models.Model):
	# Game settings
	id = models.AutoField(primary_key=True)
	SessionID = models.IntegerField()
	Player = models.ForeignKey(Player)
	Weapon = models.IntegerField(default=0)
	
	GameMode = models.SmallIntegerField(default=0, choices=((0, 'Regular Battle'), (1, 'Ranked Battle'), (2, 'Unknown (Private Battle?)'), (3, 'Unknown (Squad Battle??)')))
	Rule = models.SmallIntegerField(default=0, choices=((0, 'Turf War'), (1, 'Rainmaker'), (2, 'Splat Zones'), (3, 'Tower Control')))
	Stage = models.SmallIntegerField(default=0)
	Team = models.SmallIntegerField(default=0, choices=((0, 'Alpha'), (1, 'Bravo')))
	
	# Pre-battle / Meta
	MatchingTime = models.IntegerField(default=0)
	IsRematch = models.BooleanField(default=False)
	DisconnectedPId = models.IntegerField(null=True)
	SaveDataCorrupted = models.BooleanField(default=False)
	StartNetworkTime = models.DateTimeField(null=True)
	IsNetworkBurst = models.BooleanField(default=False)
	BottleneckPlayerNum = models.SmallIntegerField(default=0)
	MaxSilenceFrame = models.SmallIntegerField(default=0)
	# Why does Nintendo do this (Appears to be the amount of available RAM that the Wii U currently has in bytes)
	#MemoryHash = models.MaxIntegerField(null=True)
	LastBitrate = models.IntegerField(default=0)
	
	# Results
	SumPaint = models.BigIntegerField(default=0)
	IsWinGame = models.BooleanField(default=False)
	Kill = models.IntegerField(default=0)
	Death = models.IntegerField(default=0)
	Paint = models.BigIntegerField(default=0)
	RemainCount_Alpha = models.IntegerField(default=0)
	RemainCount_Bravo = models.IntegerField(default=0)
	CreatedTime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.SessionID) + ': A ' + self.get_Rule_display() + ' ' + self.get_GameMode_display() + ' played with ' + self.Player.MiiName + ' at ' + str(self.CreatedTime)