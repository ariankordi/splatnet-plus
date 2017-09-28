from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.utils.timezone import datetime
from .models import Player, Session


# Create your views here.

def PostEndpoint(request):
	UserPid = int(request.POST.get('PId'))
	try:
		player = Player.objects.get(PId=UserPid)
	except ValueError:
		return HttpResponseBadRequest('invalid')
	except Player.DoesNotExist:
		player = Player.objects.create(PId=UserPid)
	session = Session.objects.model()
	
	try:
		player.MiiName = request.POST['MiiName']
		player.Model = int(request.POST['Model'])
		player.Skin = int(request.POST['Skin'])
		player.EyeColor = int(request.POST['EyeColor'])
		player.CurrentWeapon = int(request.POST['Weapon'])
		player.Gear_Shoes = int(request.POST['Gear_Shoes'])
		player.Gear_Shoes_Skill0 = int(request.POST['Gear_Shoes_Skill0'])
		player.Gear_Shoes_Skill1 = int(request.POST['Gear_Shoes_Skill1'])
		player.Gear_Shoes_Skill2 = int(request.POST['Gear_Shoes_Skill2'])
		player.Gear_Clothes = int(request.POST['Gear_Clothes'])
		player.Gear_Clothes_Skill0 = int(request.POST['Gear_Clothes_Skill0'])
		player.Gear_Clothes_Skill1 = int(request.POST['Gear_Clothes_Skill1'])
		player.Gear_Clothes_Skill2 = int(request.POST['Gear_Clothes_Skill2'])
		player.Gear_Head = int(request.POST['Gear_Head'])
		player.Gear_Head_Skill0 = int(request.POST['Gear_Head_Skill0'])
		player.Gear_Head_Skill1 = int(request.POST['Gear_Head_Skill1'])
		player.Gear_Head_Skill2 = int(request.POST['Gear_Head_Skill2'])
		player.Rank = int(request.POST['Rank'])
		player.Udemae = int(request.POST['Udemae'])
		player.RegularKillSum = int(request.POST['RegularKillSum'])
		player.WinSum = int(request.POST['WinSum'])
		player.LoseSum = int(request.POST['LoseSum'])
		player.Region = request.POST['Region']
		player.Area = request.POST['Area']
		player.Money = request.POST['Money']
		player.Shell = request.POST['Shell']
		session.Player = player
		session.IsRematch = bool(int(request.POST['IsRematch']))
		session.SaveDataCorrupted = bool(int(request.POST['SaveDataCorrupted']))
		session.SumPaint = int(request.POST['SumPaint'])
		session.Paint = int(request.POST['Paint'])
		session.SessionID = int(request.POST['SessionID'])
		session.DisconnectedPId = (int(request.POST['DisconnectedPId']) if request.POST.get('DisconnectedPId') else None)
		session.StartNetworkTime = datetime.fromtimestamp(int(request.POST['StartNetworkTime']))
		session.GameMode = int(request.POST['GameMode'])
		session.Rule = int(request.POST['Rule'])
		session.Stage = int(request.POST['Stage'])
		session.Team = int(request.POST['Team'])
		session.IsWinGame = bool(int(request.POST['IsWinGame']))
		session.Kill = int(request.POST['Kill'])
		session.Death = int(request.POST['Death'])
		session.IsNetworkBurst = bool(int(request.POST['IsNetworkBurst']))
		session.BottleneckPlayerNum = int(request.POST['BottleneckPlayerNum'])
		session.MatchingTime = int(request.POST['MatchingTime'])
		session.MaxSilenceFrame = int(request.POST['MaxSilenceFrame'])
		session.LastBitrate = (int(request.POST['LastBitrate']) if request.POST.get('LastBitrate') else 0)
		session.Paint_Alpha = (int(request.POST['Paint_Alpha']) if request.POST.get('Paint_Alpha') else 0)
		session.Paint_Bravo = (int(request.POST['Paint_Bravo']) if request.POST.get('Paint_Bravo') else 0)
		session.RemainCount_Alpha = (int(request.POST['RemainCount_Alpha']) if request.POST.get('RemainCount_Alpha') else 0)
		session.RemainCount_Bravo = (int(request.POST['RemainCount_Bravo']) if request.POST.get('RemainCount_Bravo') else 0)
		
		player.get_face_from_request(request)
		
		player.save()
		session.save()
	except Exception as e:
		return HttpResponseServerError("error\n\n" + str(e))
	
	return HttpResponse('success')
		
def Index(request):
	players_count = Player.objects.filter().count()
	players = Player.objects.filter().order_by('-LatestTime')[:50]
	return render(request, 'index.html', {
		'players': players,
		'players_count': players_count,
		'pl_count_difference': players_count - players.count()
	})
	
def PlayerIndex(request, PId):
	try:
		player = Player.objects.get(PId=PId)
	except Player.DoesNotExist:
		return HttpResponseNotFound()
	sessions_count = Session.objects.filter(Player=player).count()
	sessions = Session.objects.filter(Player=player).order_by('-CreatedTime')[:50]
	return render(request, 'player-index.html', {
		'player': player,
		'sessions': sessions,
		'sessions_count': sessions_count,
		'se_count_difference': sessions_count - sessions.count()
	})

def SessionSummary(request, PId, session):
	try:
		session = Session.objects.get(Player=PId, id=session)
	except Session.DoesNotExist:
		return HttpResponseNotFound()
	return HttpResponse(str(session.__dict__))