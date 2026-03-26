#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF-luoja käännetylle kyberturvallisuus harjoittelu raportille
Käyttää reportlab-kirjastoa ammattimaisen PDF:n luomiseen
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
    Table, TableStyle
)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white, grey, lightgrey
from datetime import datetime

# Värit
PRIMARY = HexColor('#1a472a')
SECONDARY = HexColor('#2d5a3d')
TERTIARY = HexColor('#3d6a4d')


class PageNumCanvas(canvas.Canvas):
    """Canvas sivunumeroille"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for page_num, page in enumerate(self.pages, 1):
            self.__dict__.update(page)
            self.setFont("Helvetica", 9)
            self.setFillColor(grey)
            self.drawRightString(19.5 * cm, 1 * cm, f"{page_num}")
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


def create_translated_pdf(translated_text):
    """Luo PDF käännetystä tekstistä"""
    
    pdf_file = "Kaannetty_Kyberturvallisuus_Harjoittelu.pdf"
    
    document = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2 * cm,
        title="Käännetty Kyberturvallisuus Harjoittelu"
    )
    
    styles = getSampleStyleSheet()
    
    # Tyylit
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'],
        fontSize=24, textColor=PRIMARY, spaceAfter=12,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body', parent=styles['BodyText'],
        fontSize=10, alignment=TA_JUSTIFY, spaceAfter=8, leading=14
    )
    
    story = []
    
    # Otsikko
    story.append(Paragraph("8-Viikko Kyberturvallisuus Harjoittelu", title_style))
    story.append(Spacer(1, 12))
    
    # Jaa teksti kappaleisiin (rivinvaihdoilla)
    paragraphs = translated_text.split('\n\n')
    
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para.strip(), body_style))
            story.append(Spacer(1, 6))
    
    # Luo PDF
    document.build(story, canvasmaker=PageNumCanvas)
    
    print(f"PDF luotu: {pdf_file}")


# Käännetty teksti
translated_text = """8-Viikko Kyberturvallisuus Harjoittelu

Viikko-1

Ensimmäinen viikko fokus on Linux Windows CLI, ja perus turvallisuus työkalut. Tavoite on oppia välttämätön Linux komennot kuten ls, grep chmod tar ssh netstat find ja muut kuten että on powershell ja linux terminaali. Myös harjoittaa PowerShell komennot järjestelmä tarkastus kuten Get-Service Get-EventLog ja Get-Process. Tavoite on myös Asettaa ylös henkilökohtainen lab käyttäen VirtualBox tai VMware käyttäen Kali ja tekemällä Ubuntu ja Windows kuten kohde. Ensin minä luoda huijaus arkki top 20 komennot kanssa käyttötapaukset. Minä tehdä 10 powershell ja 10 linux terminaali. Minä tehdä lista komento huijaus arkki selittäen lyhyesti tarkoitus ja käyttö jokainen niistä ja kuvakaappaus työskentelevä lab ympäristö.                                          
Linux komennot













PowerShell komennot




















PowerShell Komennot Järjestelmä Tarkastus

Minä harjoitin välttämätön PowerShell komennot tarkastaa status ja turvallisuus aspektit Windows järjestelmä. Nämä komennot ovat tärkeä järjestelmä valvonta ja kyberturvallisuus tutkimukset.                                                  
Palvelu Tarkastus

Minä käytin Get-Service komento listata ja suodattaa järjestelmä palvelut. Tarkastelemalla palvelut auttaa tunnistaa epäilyttävä tai tarpeeton palvelut jotka voisi aiheuttaa turvallisuus riski. Tälle komento minä saada Lista kaikki pysäytetty palvelut. Tämä voi olla hyödyllinen vianmääritys tai vahvistaa että ei kriittinen palvelut ovat poistettu käytöstä.   Get-Service | Where-Object {$_.Status -eq "Stopped"} | Select-Object Name, DisplayName                                                                          


Seuraava minä oli Tarkistamassa spesifinen palvelu kuten Windows Update. Tämä Näyttää yksityiskohtainen status Windows Update palvelu (wuauserv).                         

Tapahtuma Lokin Tutkimus

Seuraava minä käytin Get-WinEvent komento joka on moderni korvaus Get-EventLog tarkastella Windows tapahtuma lokit fokus turvallisuus tapahtumat. Tälle minä nähdä Top 5 Viimeaikainen Kirjautuminen Tapahtumat Security loki. Se Etsii viimeisin 5 tapahtumat Security loki jotka vastaavat joko onnistunut (ID 4624) tai epäonnistunut (ID 4625) käyttäjä kirjautuminen. Tämä on ensisijainen askel havaita luvaton pääsy yritykset.                                                                             Get-WinEvent -LogName Security -MaxEvents 5 | Where-Object {$.Id -eq 4624 -or $.Id -eq 4625}                                                                    

Minä myös etsin virheet Application loki viimeisin 24 tuntia. Se hakee kaikki Virhe taso tapahtumat kuten Taso 2 Application loki jotka tapahtuivat viimeisin 24 tuntia.                                                         $Time = (Get-Date).AddHours(-24)
Get-WinEvent -LogName Application -FilterXPath "*[System[Level=2 and TimeCreated[@SystemTime > '$($Time.ToUniversalTime().ToString('o'))']]]"                   



Prosessi Tarkastus

Viimeksi minä käytin Get-Process komento. Se oli aktiivisesti käytetty listata ja analysoida tällä hetkellä käynnissä olevat prosessit. Tämä auttaa tunnistaa epänormaali resurssi käyttö tai tuntematon suoritettavat. Seuraava yksi listaa 5 prosessit kuluttavat eniten CPU aikaa näyttäen heidän nimi ID ja kulutettu CPU aika.                                 Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, Id, CPU


Minä vielä etsin Yksityiskohdat spesifinen prosessi kuten Chrome. Se näyttää kaikki tällä hetkellä käynnissä olevat Google Chrome sovellus prosessit mukaan lukien heidän muisti ja CPU käyttö.                                                                         Get-Process -Name chrome







Luomassa lab ympäristö

Viimeinen mutta ei vähäisimpänä minä oli luomassa lab ympäristö Virtualbox. Minä oli Lataamassa Kali Linux kanssa tarvittu asetukset. Minun kohde tulee olemaan windows 10 joka jo olemassa virtualbox. Testata että lab ympäristö toimii minä tein ping komento kanssa Kali Linux ja Windows 10. Kali Linux minä tein ping -c 4 10.0.2.5 komento joka vastaanotti positiivinen loppu tulos. Minä tein se väärä ip osoite kanssa myös joka teki epäonnistuminen yritys. Windows 10 minä tein ping -n 4 10.0.2.15 komento joka myös päättyi positiivinen tulos. Tämä myös minä yritti väärä ip osoite kanssa todiste että molemmat virtuaali laite kommunikoi yhdessä valmis kyber turvallisuus testaus. Minä myös tein sudo nmap -sV 10.0.2.5 komento kohti Windows 10. Tämä yksi tekee skannaus että mitkä portit ja palvelut ovat tällä hetkellä avoinna sillä windows. Kuten voidaan nähdä esimerkiksi microsoft edge web selain oli avaamassa sillä hetkellä. Nyt lab ympäristö on asetettu ja valmis tuleva viikko testaus kanssa komento virtualbox. Jälkeen kaikki paljon oppiminen uusista asioista ja enemmän kuin jännittävä oppia enemmän etninen hakkeroinnista ja miten kyber turvallisuus toimii.                                








Viikko-2

Verkosto & Tiedustelu

Tämä viikko fokus on Skannaus ja luettelointi toimet. Tavoite on oppia perusteet TCP/IP ja portit Käyttää nmap skannata isännät ja tunnistaa avoin portit ja palvelut oppia whois dig ja nslookup DNS tiedustelu ja automatisoida yksinkertainen skannaus raportti generointi Bash skripti. Seuraava minä tehdä joitakin testaus niitä varten samalla selittäen jokainen että mitä minä tein miten se toimii ja mitä minä sain loppu tulos.    
skannaus palvelut (Nmap)

Ensin minä avasin molemmat virtuaali laitteet jonka jälkeen minä käytin Kali Linux missä minä uudistin sudo nmap -sV 10.0.2.5 työkalu komento nähdä avaavat portit ja palvelut Windows 10. Kuten voidaan nähdä kuvakaappaus jälkeen komento minä voin nähdä avoin portit Windows 10 sama kuin avoin palvelut. Myös mac osoite ja käytetty alusta joka tämä tapaus on virtualbox. Yhteenveto Nmap paljastaa mitkä palvelut kuten HTTP SMB tai RDP ovat avoinna ja mitkä ohjelmisto versiot ovat käynnissä niitä. Tämä tieto auttaa tunnistaa mahdollinen haavoittuvuudet.                                                         

Minä myös tein komento sudo nmap -sV -p- 10.0.2.5
# -sV: Tunnistaa palvelu versio.
# -p-: Skannaa KAIKKI 65535 portit (voi ottaa pitkä aika, voit rajoittaa esim. -p1-1000)                                                                             Tämä on samanlainen yksi jonka minä tein ennen mutta antava enemmän yksityiskohtainen tieto ja se on enemmän hyvä tapa saada tieto avoin portit ja palvelut Windows 10 samalla tietäen heidän nykyinen tilanne.                                  

Seuraava komento minä tein oli sudo nmap -sC -sV 10.0.2.5
# -sC: Suorittaa oletus skriptit
Tämä on Oletus Skriptit skannaus missä minä käytin Nmap:n sisäänrakennettu skriptit perus haavoittuvuus skannaus kuten SMB skannit. Loppu tulos oli vähän erilainen kuin viimeiset antava enemmän tieto Windows 10 tilanne jos joku haluaisi tehdä kyber hyökkäys sitä vastaan.                                                        

WHOIS organisaatio Tiedot ja DNS Kyselyt
Seuraava minä tein pieni testi WHOIS organisaatio Tiedot. Mitä minä tein oli etsimässä tieto domain nimi käyttäen komento whois google.com. Sen jälkeen minä tein DNS kyselyt (A/MX/NS tietueet) käyttäen komento dig google.com A # Saa A tietue (IP osoite)                                                       dig google.com MX # Saa posti palvelimet
nslookup google.com # Perinteinen haku
Näiden jälkeen minä sain perus tieto Google jonka minä avasin Windows 10 näkemässä tilanne siitä kanssa Kali Linux ja mahdollinen heikko kohdat kyber hyökkäys mutta tässä tapaus oppia mitä on tärkeä suojata kun haluaa olla turvallinen verkossa.                                                                  Bash Skripti ja Raportti Generointi

Viimeinen testi minä tein oli luomassa yksinkertainen Bash skripti automatisoida skannit ja tallentaa tulokset. Ensin minä annoin komento # 1. Määritä kohde (Windows 10 IP) TARGET_IP="10.0.2.5" # 2. Määritä raportti nimi ja polku REPORT_FILE="nmap_report_$(date +%Y%m%d_%H%M%S).txt" echo "--- Aloittamassa Nmap skannaus kohde $TARGET_IP ---" > $REPORT_FILE echo "Päivämäärä: $(date)" >> $REPORT_FILE # 3. Suorita Palvelut/Versiot Skannaus ja liitä tulos raportti sudo nmap -sC -sV $TARGET_IP >> $REPORT_FILE echo "--- Skannaus täydellinen. Raportti tallennettu tiedosto $REPORT_FILE ---"        Sen jälkeen minä annoin ls –l komento nähdä että skripti minä tein on tallennettu tiedostot ja viimeksi minä annoin cat nmap_report_20251023_110405.txt komento nähdä mitä skripti kertoo Windows 10 portit ja versiot siitä. Kuten voimme nähdä lopullinen raportti IP osoite on Windows 10 kertova perus tilanne siitä. Ei paljon nähdä mutta se on perus virtualbox laite. Vielä on perus testi miten tehdä skriptit ja saada tieto kohde sinä olet etsimässä ei vahingollinen tapa tämä aika mutta miten suojata se paremmin vastaan mahdollinen hyökkääjät.                                                               

Verkosto Teknologiat ja Tiedustelu Teoria

Viimeinen mutta ei vähäisimpänä minä kerron vähän tiedustelu vaihe kuten skannaus sisältää kartoitus kohde käyttäen perustavanlaatuinen verkosto protokollat (TCP/UDP) ja portit. Minä käyttää yksinkertainen arkkeja kertoa perus tieto niistä täyttääkseen aiheet jotka tarvitsevat kattaa.                                                               
A. Protokollat: TCP vs. UDP








B. Portit ja Palvelut

Portti on looginen kommunikointi kanava tunnistettu numero (0-65535) takana IP osoite. Se erottaa eri sovellukset ja palvelut käynnissä isäntä kone. Tässä yksinkertainen tapa näyttää niistä.             
Joitakin avain esimerkkejä

Kietomassa viikko 2

Suoritettu toinen viikko tehtävät tietäessä kyberturvallisuus projekti minä olen siirtynyt tehokkaasti laboratorio asetus aktiivinen tiedustelu ja verkosto kartoitus yksinkertainen esimerkit. Kaikki tämä motivoi minua uusi taso oppia enemmän kyber turvallisuus kunnes kaikki tehtävät ja aiheet on tehty loppuun.                                                                           
Aiheet minä opin Tämä Viikko
Verkosto tiedustelu Perusta. Minä vahvisti että tehokas tunkeutuminen testaus aina alkaa perusteet. Kaikki alkoi onnistunut ping testit vahvisti kaksisuuntainen kommunikointi Kali Linux ja Windows 10 tekemällä minun kohde elinkelpoinen tuleva testaus.                                       Nmap tuli työkalupaketti. Minä opin käyttää Nmap kanssa -sC -sV liput kerätä aktiivinen älykköys sen sijaan passiivinen data. Tuloksena oleva raportti nmap_report_*.txt ei ole vain lista avoin portit mutta se on luettelo aktiivisesti käynnissä olevat palvelut kuten SMB tai RDP ja heidän versiot. Tämä on kartta Windows 10 kohteiden puolustukset.                                                                    Tehokkuus Läpi automaatio luomalla ja suorittamalla Bash skripti jonka minä osoitin kyky automatisoida toistuva tehtävät varmistamalla aika tehokkuus ja johdonmukainen dokumentoitu tulos aloitus tuleva enemmän tieto kyberturvallisuus työ.                                                                            Viikko-3

Minä aloittaa kolmas viikko teoria kanssa haavoittuvuus Skannaus ja raportointi. Minä tehdä yksinkertainen lista OWASP top 10 ja haavoittuvuus raportit. Sen jälkeen minä siirtyä pitkin Nikto ja Nuclei asentaminen skannaus ja testaus. Viimeinen yksi minä tehdä Pentest raportti pohja oma henkilökohtainen tieto sillä.           
A. OWASP Top 10

Tämä yksi on konsensus dokumentti joka listaa kymmenen kriittisin turvallisuus riskit web sovellukset. Se on teollisuus standardi käytetty priorisoida arvioinnit ja luokitella tulokset. Seuraava malli minä kerron vähän siitä.            
B. Tulkitsemassa Haavoittuvuus Raportti

Tämä osio minä myös selitän vähän raportti tuotettu haavoittuvuus skanneri jotka ovat Nikto ja Nuclei. Miten lukea se ja miten pitäisi aina tulkita läpi riskit.                                                    

Asentamassa ja Käyttämässä Haavoittuvuus Skannerit

Yleensä sekä Nikto että Nuclei työkalut on jo asennettu Kali Linux mutta minä halusin tehdä varma minun virtuaali kone versio. Minä tarkistin molemmat tai ne ovat ja minä myös tarkistin heidän päivitykset. Sitten minä tein yksinkertainen skannaus ja raportti testi sekä kanssa.                                                  Minä aloitin Nikto kanssa. Ensin minä annoin komento sudo apt update
sudo apt install nikto –y tehdä varma päivitykset tämä työkalu. Sen jälkeen minä annoin komento nikto -h http://10.0.2.5 -o nikto_report_w10.txt -F txt. Loppu tulos oli näyttämässä kuten tämä todiste että työkalu on asennettu päivitetty ja työskentelevä Kali Linux.                                                                  

Seuraava minä tein samanlainen toiminta Nuclei kanssa. Vähän siitä työkalu se on kuten Nikto mutta nopeampi ja joustavampi malli perustuva skanneri. Se ei suorita perinteinen web haut mutta sen sijaan etsii spesifinen tunnettu haavoittuvuudet CVEs käyttäen YAML-pohjainen mallit. Nuclei on sopiva sekä web sovellukset että verkosto infrastruktuuri.                                               Ensin minä tein sama kuin Nikto varten tekemällä varma Nuclei työkalu on Kali Linux kanssa päivitykset. Minä tein se kanssa komento sudo apt update                          sudo apt install nuclei -y
nuclei -update-templates
Sen jälkeen minä tein komento # 1. Luo kohde lista
echo "http://10.0.2.5" > targets.txt

# 2. Suorita skannaus kohde lista ja tallenna tulokset
nuclei -l targets.txt -severity high,critical -o nuclei_report_w10.txt. Nämä kaksi komento kuten todiste että myös nuclei työkalu toimii Kali Linux jonka minä käytän osa tämä lab valmis tehdä skannaus ja raportointi Windows 10 joka on kohde tämä projekti.                                                              


Penetration test report

Minä kietoi viikko 3 tehtävät samalla tein tunkeutuminen testi raportti kyber turvallisuus löydöt jälkeen tekemällä testi komennot nikto ja Nuclei. Mitä minä huomasin jälkeen nämä testit oli esimerkiksi että Windows 10 ja microsoft edge web selain sillä eivät ole heidän paras tai viimeisin kyber turvallinen taso merkittävä hakkereita ja muut mahdollinen hyökkääjät on enemmän helppo heidän pahat tarkoitukset vastaan käyttäjä. Se on hyvä asia tämä vain virtualbox ja ei pää käyttö mutta tämä tapa minä voin myös tehdä raportteja minun pää isäntä PC näkemässä se kyber turvallisuus tilanne ja tietäen miten suojata se paremmin vastaan mahdollinen hakkereita. Kerran taas uusi viikko antoi paljon oppia motivaatio oppia enemmän ja kehittyä paremmin tieto kanssa kyber turvallisuus joka on vain enemmän tärkeä koska teknologia kehittyy kasvaa ja niin tekee rikolliset myös mutta hyvä puoli aina yksi askel enemmän eteenpäin.                                










Viikko-4

Johdanto Web Hyökkäys’

Tämä viikko aiheet fokus on yleiskatsaus ja testaus ympäristö. Mitä että tarkoittaa on muuttamassa kerätty tieto käytännöllinen hyökkäykset. Koska edellinen skannit ei havainnut aktiivinen web palvelin Windows 10 kuten kohde testaus on ohjattu turvallinen tarkoituksella haavoittuva käytäntö ympäristöt. Alla on lista erilainen testaus alustat.                                                    

Ydin Web Hyökkäys Konseptit

Tämä vaihe fokusoi yleisin haavoittuvuudet listattu OWASP Top 10 jonka minä oli mainittu aikaisempi viikko. Seuraava malli selittää vähän XSS joka on Cross-Site Scripting ja vähän SQL Injection.                          



Tulevat ne minä vielä kerron vähän perusteet Tiedosto Lataus Haavoittuvuudet ja Brute Force Hyökkäykset.                                                          









Komennot Kohdistettu Windows 10 VM

Sen jälkeen teoria osio minä tein joitakin komento esimerkit missä kohdistettu windows 10. Kuten aina ei hyökkäys merkittävä mutta löytämässä erilainen tavat jotka mahdollinen hyökkääjät voisi käyttää ja jotka vuoksi nämä aiheet ovat tärkeä pitää mieli suojata todellinen isännöinti laite enemmän paremmin jotta data tiedostot jne pysyy enemmän suojattu nyt ja tulevaisuudessa.                                                                
Ensimmäinen komento minä tein oli sudo nmap -p 445,3389 10.0.2.5 missä Tulos näyttää Portti 445/tcp kuten avoin ja tunnistava palvelu kuten microsoft-ds tai netbios-ssn. Portit jotka ovat käytetty ovat SMB (139, 445) ja RDP (3389) ja käytetty työkalu on nmap. Mitä saaminen jälkeen komento on yksinkertainen mutta todiste että miten se toimii ja voi antaa tarvittu tieto kohdistettu laite.                                           







Seuraava yksi minä olin etsimässä luettelointi ja hyökkäys. Ensin minä annoin enum4linux -U 10.0.2.5 komento missä käytetty työkalu oli enum4linux. Tavoite tälle komento on yrittää luetteloida lista käyttäjä tilit Windows kohde kautta SMB. Tulos näyttää lista käyttäjänimiä tai Domain Käyttäjät kuten Administrator Guest jne. Tämä on vahva todiste onnistunut luettelointi vaikka tuleva virhe myös voi olla koska windows 10 palomuuri ja muut suojat jotka ovat aina jokin taso sen sijaan olla täysin avoin hyökkääjät.                        


Sen jälkeen yksi minä yritti Brute Force Hyökkäys demonstrointi vastaan SMB. Minä annoin komento hydra -l Administrator -P /usr/share/wordlists/rockyou.txt smb://10.0.2.5 samalla käyttäen hydra työkalu. Tarkoitus tälle komento on yritykset arvata Administrator salasana käyttäen kuuluisa rockyou.txt sanasto. Tulos näyttää smb://10.0.2.5:445 isäntä: Administrator pass: [CRACKED_PASSWORD] merkki onnistunut yritys tai selkeä status yritykset demonstroiva tekniikka. Mitä minä sain ei ollut cracked salasana mutta myös voi olla koska windows 10 suojat. Vielä teoria taso sai hyvä näkymä miten hakkereita voi löytää tapoja crack käyttäjien salasanat osa prosessi.                                      












Viimeksi minä tein erilainen tyyppi komento kuten yksi lista. Minä laitoin perus Yhteyttä (W1/2) kanssa ping -c 4 10.0.2.5 testi jonka jälkeen Löytö (W2/3) kanssa sudo nmap -p 139,445,3389 10.0.2.5 komento. Sen jälkeen minä vielä laitoin Luettelointi/Hyökkäys (W4) kanssa enum4linux -u "Administrator" -p "YourPassword" 10.0.2.5 jonka jälkeen Brute Force Demo (W4) kanssa hydra -l Administrator -P /usr/share/wordlists/rockyou.txt smb://10.0.2.5 -t 4 laittamalla kaikki komennot kuten yksi lista. Minä myös etsin vähän XSS Todiste (W4) ja SQLi Todiste (W4) kuten Ulkoinen Web Kohde. Kaiken jälkeen nämä minä sain hyvä näkymä miten hakkeri aloittaa opiskella heidän kohde samalla löytämässä tapoja päästä sisään käyttäjien profiilit ja sitten tehdä heidän paha toiminta tapahtua. Kaikki että tarvitsee olla enemmän ja enemmän varovainen sama kuin todellinen maailma missä on mahdollista elää ilman kokeilla rikollinen. Sama on mahdollista verkossa kun tietäen mitä tehdä ja miten pysyä suojattu vastaan rikolliset.                       




HYÖKKÄYS RAPORTIT

A. Todentunut Käyttäjä Luettelointi (Windows 10 VM)

Löytäminen tieto paljastaminen kautta SMB Luettelointi
Kohde Ympäristö oli Windows 10 VM
Kohde IP oli 10.0.2.5
Haavoittuvuus Tyyppi oli tieto paljastaminen ja turvallisuus väärinmääritys (SMB Luettelointi)                                                                   Vakavuus oli KESKIVAIKEA
OWASP / Mitre Viite oli Mitre ATT&CK T1087.001 - Tili Löytö paikallinen tili kautta. Server Message Block (SMB) palvelu (Portti 445) Windows 10 kohde vaikka ei sallinut anonyymi yhteydet salli sisäinen järjestelmä tieto poisto mukaan lukien workgroup nimi ja lista paikallinen käyttäjä tilit kun annettu kelvollinen tunnistetiedot. Tämä on kriittinen tieto paljastaminen joka avustaa seuraava kohdistettu hyökkäykset.                              




Todiste Konsepti (PoC)

Minä käytin Nmap vahvistaa SMB palvelu oli aktiivinen Portti 445. Enum4linux työkalu oli suoritettu kanssa tunnettu hallinnollinen tunnistetiedot ohittaa oletus autentikointi este. Komento onnistui tunnistaa workgroup (CYBERSE) ja hakea lista paikallinen käyttäjät mukaan lukien järjestelmä tilit kuten Guest ja Administrator ja potentiaalisesti mikä tahansa mukautettu tilit.                                 
Korjaus Suositus

Poista etä luettelointi tilit ja jaot kautta Group Policy (GPO) missä mahdollista ja varmista vahva salasana politiikka estää käyttö luetellut käyttäjänimet sanakirja tai brute-force hyökkäykset kuten käyttäen hydra työkalu.                                                                          

B. Heijastettu Cross-Site Scripting (Web Sovellus)

Löytäminen heijastettu XSS Haavoittuvuus. Kohde Ympäristö oli haavoittuva Web Sovellus kuten TryHackMe: Web Fundamentals. Kohde oli URL/Osoite: http://[TARGET_IP]/vulnerabilities/xss_r/?name=                                                Haavoittuvuus Tyyppi oli heijastettu Cross-Site Scripting (XSS). Vakavuus oli KORKEA  

Kohde web sovellus haku ominaisuus epäonnistui asianmukaisesti desinfioida tai koodata käyttäjä syöte ennen heijastamalla se takaisin asiakkaan selain. Tämä vika mahdollistaa hyökkääjä upottaa vahingollinen JavaScript koodi URL joka suorittaa kun uhri napsauttaa linkki.                                                    
Injektio Piste: Tunnistettu syöte kenttä joka heijastaa käyttäjä data suoraan HTML sivu.                                                          Payload Käytetty: Seuraava JavaScript payload oli upotettu haavoittuva parametri                                                                       Onnistunut Suoritus: Kun URL sisältävä payload oli ladattu selain suoritti skripti.                                                           Vaikutus: Vakio JavaScript hälytys laatikko ilmestyi todistaen että hyökkääjä voi suorittaa mielivaltainen asiakas-puoli koodi joka voisi olla hyödynnetty istunto sieppaaminen tai tunnistetieto varkaus.                                                           

Korjaus Suositus

Ensisijainen Korjaus: Ota käyttöön vankka konteksti-tietoinen ulostulo koodaus kaikki käyttäjä-syötetty data. Kaikki erityis merkit (<, >, /, ", ') täytyy muuntaa heidän HTML entiteetti vastineet ennen näyttämistä sivu.                           Sisältö Turvallisuus Politikka (CSP): Ota käyttöön rajoittava CSP otsikko rajoittaa mitkä lähteet ovat luotettu suorittaa skriptit merkittävästi lieventäen vaikutus mikä tahansa jäännös XSS haavoittuvuudet.                                                   Kerran taas viikko oli täynnä suuri oppiminen tekemässä uusia ideoita tuleva viikot haluava antaa enemmän kunnes loppu projekti kanssa enemmän jännittävä tunne joka jälkeen vahva perus tieto kyber turvallisuus ja se tarvitsee nyt ja tulevaisuudessa.  










Viikko-5

Etuoikeus Eskalaatio & Skriptaus

Tämä viikko siirtää fokus web sovellukset itse käyttöjärjestelmä. Tavoite on simuloida skenaario missä hyökkääjä on saanut matala-taso pääsy Linux kone kuten kautta web shell tai heikko SSH salasana ja yrittää nostaa hänen etuoikeudet standardi käyttäjä root. Käytäntö tulee olla suoritettu haavoittuva Linux koneet alustat kuten TryHackMe tai Hack The Box.                                                                    
Tieto Keräys (Luettelointi) Tutki perusteellisesti järjestelmä heikkoudet kuten käyttäjät tiedosto oikeudet ajurit ja verkosto yhteydet.               Vektori Tunnistus: Tunnista elinkelpoinen hyökkäys polku kuten väärinmääritetty SUID tiedosto ja haavoittuva PATH asetus.                                             Hyökkäys Suorita hyökkäys saavuttaa root etuoikeudet.

Yleinen Linux Etuoikeus Eskalaatio Vektorit

Tämä osio minä kerron vähän teoria SUID (Set-User-ID) Bit Hyökkäys PATH Muuttuja Manipulaatio ja Cron Työt (Ajoitettu Tehtävät) Hyökkäys. Jokainen niistä minä kerron heidän perusteet jotka ovat Konsepti Haavoittuvuus Tunnistus ja Korjaus.                                                                   

SUID (Set-User-ID) Bit Hyökkäys


PATH Muuttuja Manipulaatio


Cron Työt (Ajoitettu Tehtävät) Hyökkäys



Komento Sarja Järjestelmä Luettelointi

Seuraava komennot ovat suoritettu kohde Linux järjestelmä kuten TryHackMe kone jälkeen saavuttanut matala-taso shell. Ensimmäinen komento minä annoin oli find / -perm -4000 -type f 2>/dev/null joka etsii kaikki binäärit kanssa SUID bit joka usein tarjoaa helpoin polku root. Etsimällä tiedostojärjestelmä juuri (/) kaikki tiedostot (-type f) jotka ovat SUID oikeudet asetettu (-perm -4000). Virheet ovat tukahdutettu (2>/dev/null). Tulos tämä komento pitäisi olla Lista binäärit kuten /usr/bin/pkexec, /usr/bin/passwd. Kuten loppu tulos minä sain selkeä lista niistä kuten ne.                                                                          

Tarkistamassa Cron Työt

Seuraava tuleva komennot paljastaa ajoitettu skriptit jotka ovat usein suoritettu root. Ensimmäinen komento minä annoin oli ls -la /etc/cron* joka antoi listat kaikki cron työ tiedostot ja hakemistot, paljastava oikeudet. Onnistunut tulos näyttää tiedosto omistus (root root) ja luku/kirjoitus oikeudet. Toinen komento jälkeen että minä annoin oli cat /etc/crontab joka tulostaa sisältö järjestelmä pää crontab tiedosto. Kun tehty oikein Se Näyttää komento rivit ja ajoitus ajat usein suoritettu root käyttäjä. Mitä minä sain terminaali oli täsmälleen kuten ne.                             



Näiden jälkeen komennot minä vielä annoin sudo –l yksi joka määrittää mitä komennot nykyinen käyttäjä voi suorittaa root (sudo). Onnistunut tulos pitäisi olla Lista sallittu komennot kuten (ALL) NOPASSWD: /usr/bin/cat). Mitä minä laitoin Kali Linux terminaali antoi loppu tulos kuten tämä.                                             

Automatisoitu Etuoikeus Eskalaatio Skripti

Tämä bash skripti kietoo pois viikko 5 aiheet. Minä myös laitoin video viikoittainen raportti osio näyttää enemmän kaikki mitä minä löysin jälkeen painamalla enter nappi seuraava skripti. Kaikki minä toivon on että minä ymmärrän aiheet jokainen viikko antaa enemmän niistä kuin minä annan. Jo top puoli kyber turvallisuus projekti joka niin pitkälle on jättänyt enemmän kuin hämmästyttävä tunne sisällä enemmän luottamus tuleva viikot. Kaikki tämä on kehittynyt minua kyber turvallisuus. Koska minä aloitin minun opiskelu kyber turvallisuus oli yksi minun pää kiinnostus. Kuten paljon teknologia kasvaa niin tekee kyber turvallisuus. Ne takana se ovat kuten digitaalinen laki virkamiehet tekemässä varma että käyttäjät ovat aina turvallinen yksi askel eteenpäin kuin hyökkääjät ja hakkereita jotka tarvitse ottaa vakavasti.                                        

Viikko-6

Puolustava Turvallisuus ja loki analyysi kanssa Blue Team Perusteet

Tämä viikko sisältää siirtyminen hyökkääjä joka esimerkki on punainen tiimi puolustaja joka on sininen tiimi. Loki analyysi on kulmakivi puolustava turvallisuus koska järjestelmä lokit tarjoavat lopullinen todiste epäonnistunut hyökkäykset ja onnistunut rikkomukset. Tehokas loki kokoelma ja analyysi mahdollistaa poikkeavuudet havaitseminen kuten Brute Force hyökkäykset tai epätavallinen prosessit suoritus. Seuraava arkki minä näytän vähän loki virta ja SIEM Kontekstuaalinen.                   

Kriittinen Järjestelmä Lokit ja Indikaattorit

Windows tapahtumat ovat luokiteltu ja annettu spesifinen numeerinen tapahtuma IDt. Seuraava arkki minä näytän vähän Windows Lokit myös tunnettu kuten tapahtuma katselija.           Linux lokit toisaalta ovat tyypillisesti tallennettu teksti tiedostot /var/log/. Seuraava arkki minä näytän vähän siitä myös.                                         

Komento Sarjat etsiä Epäonnistunut Kirjautuminen ja poikkeavuudet

Seuraava komennot täyttää vaatimus käyttää PowerShell ja Bash löytää epäonnistunut kirjautuminen ja epänormaali prosessit. Minä näytän esimerkit molemmat aloitus Windows Powershell.                                                             
Etsi epäonnistunut kirjautuminen windows powershell

Windows Powershell minä käytin `Get-WinEvent -FilterHashtable @{LogName='Security' ; ID=4625; StartTime=(Get-Date).AddDays(-1)} komento suoritettu Windows 10 VM kerätä loki data. Mitä se antoi oli Format-List -Property TimeCreated Message` kanssa Suodattaa Security loki kaikki Tapahtuma ID 4625 tapahtumat viimeisin 24 tuntia ja näyttää aika ja spesifinen epäonnistuminen viesti. Mitä minä sain oli näyttämässä kuten tämä.                                                                    



Etsi Epäonnistunut SSH Yritykset Linux

Seuraava minä suoritin Linux kohde kerätä loki data. Sille minä olin käyttämä sudo grep "Failed password" /var/log/auth.log komento. Sen jälkeen minä sain pieni lista kirjautuminen historia. Koska virtuaali kone ja ei isäntä kone lista on pieni mutta vielä antaa idea miten löytää ulos kirjautuminen historia sinun laite myös näkemässä jos joku muu on yrittänyt kirjautuminen joka voi olla tunnistamaton.                   

Puhumassa siitä Jotta suoritettu Linux kohde etsiä epäilyttävä kuunteleva portit kuten reverse shell minä vielä tein `netstat –tuln komento. Sen jälkeen tuli enemmän yksityiskohtainen lista kirjautuminen tämä virtuaali kone. Kuten voidaan nähdä ei ole kukaan joka minä voin tunnistamaton merkittävä tämä laite on ollut turvallinen ilman uhka hakkeri jne.                                                            




Loki Jäsennys Skripti Brute Force Hälytys

Kietomassa viikko 6 aiheet viimeinen niistä minä tein pieni demo miten nähdä jos on Brute Force hälytys sinun laite nähdä onko joku yrittänyt hakkeroida se. Antaa lyhyt esimerkki sille ensin minä tein Kali Linux terminaali ls -lah /usr/share/wordlists komento joka on lista sisäänrakennettu Kali sanastot. Sen jälkeen minä tein komento zcat /usr/share/wordlists/rockyou.txt.gz | head -n 200 komento joka on yhteinen rockyou lista. Sen jälkeen minä Asensin ja latasin suuri julkinen SecLists kokoelma Kali Linux terminaali kanssa sudo apt update && sudo apt install -y seclists                                                            # —tai— kloonaa GitHub repo (jos haluat viimeisin kopio)
git clone https://github.com/danielmiessler/SecLists.git ~/SecLists
ls -lah ~/SecLists/Passwords. Sen jälkeen yksi minä tein mukautettu käyttäjänimi lista missä korvasin nimet kanssa sinun kohde-hyväksytty lista. Minä tein se kanssa komento printf "alice\nbob\ncarol\njohn.doe\njdoe\n" > ~/wordlists/usernames-target.txt wc -l ~/wordlists/usernames-target.txt. Sen jälkeen kaikki tämä otti oma aika ladata ja asentaa mutta jälkeen että minä sain esimerkki lista käyttäjistä. Red marked are ones who can be sing for possible hacker who want to harm device and users on it. This week eas once again full of important learning about of cyber security and how to be more alert and more focysed for own online safety. Only small amout of project remaining but so far learning new has gave big ideas what to do when real opportunities comes for career and over all everyday life while using own devices.  
Week-7

Security Automation Project

This week culminates in the development of a functional automation script that connects learned security concepts into a single efficient workflow. This project demonstrates the ability to scale security testing moving from manual command execution to automated and reproducible reporting.                               
Automated Recon and Report Tool

Choise of project for me is topic above. Target is to focus on active reconnaissance against a target web server. Sheet below I tell a bit how everything will go.                                                                              
Automation and Tool Integration

The key to this project is using the power of Bash to link specialized tools together and manage their output. Next I tell bit about of used tools purpose of them and how they work.                                                           
A. Nmap XML Output (Data Extraction)
To integrate nmap results into an automated report I use the -oX flag.
Command is nmap -oX output.xml target
Purpose for this is to tell Nmap to save the scan results in an XML format which is easily parsed by scripts like using tools like grep and regular expressions to extract specific data such as open ports and services.                       
B. Gobuster and Directory Fuzzing

Gobuster is used to brute-force directories and file names. For automation the key is to ensure the output is saved to a file using the standard redirection operator.                                                                          Command is gobuster dir -o output.txt -u target -w wordlist
Purpose is that The -o output.txt flag ensures all discovered paths are saved to a clean parsable text file.                                                    

C. Bash Scripting for Reporting

The core script uses Bash features to:
Define Variables to store the target IP output files and directories.
Execute Tools are run nmap and Gobuster sequentially.
Pipe Data is to use commands like grep sed and awk to extract only the relevant findings from the raw output files.                                             Generate File is to use echo commands and >> redirection to construct the final readable Markdown report (.md).                                                 
This example shows how to create script file on Kali Linux. I opened nano editor on terminal after giving nano auto_recon.sh command. After that editor section opened. I placed needed script on there where IP address of Windows 10. After that I pressed ctrl+s to save it and then ctrl+x to exit from editor. After that when I gave chmod +x auto_recon.sh command which sets execute permissions. After that I gave ./auto_recon.sh 10.0.2.5 command. That one runs the Automated Reconnaissance Script. The command executes the script using targeted IP address. script runs nmap and gobuster against 10.0.2.5 and generate needed final report.    

After making small automated reconnaissance and reporting tool project for week 7 I am more than ready for coming last one. I have gave everything even when not still professional level about of cyber security. What I still have done is lots of learning new with high motivation to continue towards my comiing career which can be cyber security. What I know is that topic like that is only more needed and more big needing more professionals on it where I want to give my own part now and in the future.                                                Week-8

Final Project and Presentation

1. Executive Summary and Final Report Structure

Coming two pages or more I focus final report with summary about of automated Reconnaissance and Reporting Tool which I selected as a main project to wrap cybersecurity Interns section. I tell bit about of main topics with basic information where focusing most important parts to give good full vision for it. After that I make about 10 minute long demo for final project which after giving end speak with final feelings how I feel after all week tasks what I learned and how it motivates me for coming future career.                                           







Final Project Report automated reconnaissance and reporting tool
Project Title Security Operations and Automation Capstone Project
Primary Focus Integration of Offensive Security (Red Team) Reconnaissance with Defensive Security (Blue Team)                                                    Reporting Author Aleksis Kauranne October 30, 2025

1. Executive Summary
This project successfully developed and implemented the Automated Reconnaissance and Reporting Tool a bespoke Bash script designed to significantly streamline the initial phase of penetration testing and vulnerability assessment. The ART tool automates active network and web enumeration consolidating complex technical findings into a clean human readable Markdown report.                           The project demonstrates proficiency in shell scripting open source tool integration which are Nmap and Gobuster data parsing and structured security reporting. The final solution reduces manual effort ensures consistent methodology and provides immediate actionable intelligence for security teams. The primary technical challenges data normalization and error handling in a sequential script were successfully overcome proving mastery of the core project objectives.            
2. Project Context and Objectives
The foundational goal of this capstone project was to unify the technical skills acquired across both offensive (Red Team) and defensive (Blue Team) modules. Specifically, the project aimed to solve the common security operations problem of translating raw scanner output into a format suitable for executive review or immediate mitigation efforts.                                                    
Core Objectives
Automation Replace manual execution of command line tools with a robust reproducible script.                                                                    Integration Successfully integrate industry standard tools which are nmap and gobuster within a single workflow.                                                Normalization Parse disparate output formats (Nmap XML and Gobuster text) into a unified structure.                                                             Reporting Generate a clear well structured final report (Markdown) suitable for documentation and auditing.                                                     Demonstration Present a functional, reliable solution in a live environment.    

3. The Solution of Automated Reconnaissance and Reporting Tool
The ART script is a modular solution built entirely in Bash emphasizing speed portability and minimal dependencies. The script operates in a three-stage sequence which I tell bit about of coming section.                                     
Stage 1 Deep Port and Service Scanning (Nmap)
Command nmap -p- -sV -T4 <Target_IP> -oX nmap_output.xml
Function Performs a comprehensive full-port scan (-p-) and service version detection (-sV) against the target. The critical element is the use of the -oX flag to output results in XML format which simplifies subsequent machine based parsing.                                                                               Stage 2 Web Directory Enumeration (Gobuster)
Command gobuster dir -u http://<Target_IP> -w <Wordlist> -o gobuster_output.txt 
Function Executes brute-force directory discovery against web ports identified by Nmap. The output is redirected to a plain text file for easy filtering.       Stage 3 Parsing and Report Generation (Bash Logic)
Logic Bash commands (grep, awk, sed) are used to analyze the temporary data files.                                                                              The Nmap XML is filtered using grep and awk to extract only open ports service names and version numbers.                                                       The Gobuster text file is filtered to retain only successful or interesting status codes (200, 301, 403).                                                       Output The extracted data is systematically written into the final REPORT_FINAL.md file creating a professional sectioned document that requires minimal post-processing.’                                                                      
4. Analysis Key Findings and Recommendations
The execution of the ART tool against a typical lab target which on this case windows 10 IP address 10.0.2.5 consistently revealed key vulnerabilities that require immediate attention.                                                        Generic Findings (Based on Simulated Output)
Service Exposure A full-port scan routinely identifies non standard or unexpect ed ports open to external connectivity like FTP on port 21 or a secondary HTTP server on port 8080.                                                              Version Identification Version detection often exposes outdated or unpatched software like Apache 2.4.x which may have known vulnerabilities.                   Hidden Resources Directory fuzzing frequently uncovers sensitive or misconfigure d paths such as administrative panels (/admin) backup directories (/backup) or development notes (/dev).                                                        Security Recommendations
Based on the capabilities of the ART tool the following general security recommendations are provided which I show on coming sheet.                             

5. Reflection Challenges and Future Work
Challenges Encountered
The most difficult technical challenge was dealing with the unstructured and proprietary nature of tool outputs.                                                Nmap XML Parsing While XML is structured extracting specific attributes like service version from nested tags required careful use of grep and awk which is often fragile.                                                                      Error Handling Ensuring the script could gracefully handle execution failures like target offline permissions errors or tool not installed required adding comprehensive check_tool functions and exit clauses.                                 Time Efficiency Balancing the need for a comprehensive full-port scan (-p-) against the time constraints of a fast automation tool required conscious optimization of Nmap timing (-T4).                                                        Key Learnings
Personally which I feel the most this project reinforced several critical cybersecurity and scripting concepts.                                                 Data Normalization The ability to take data from any source and force it into a required structure (Markdown) is essential for operational efficiency.          Bash Proficiency The power of combining simple utilities like grep sed and awk for complex data manipulation proved far more efficient than relying on higher level languages for basic scripting tasks.                                        Blue Team Value The true value of a Red Team tool is realized only when it delivers clear standardized reports that a Blue Team can use to immediately prioritize defenses.                                                                     
Future Development Goals
To evolve the ART into a fully production ready vulnerability management solution the following enhancements are planned ready for my possible future needs.    SIEM Integration Modifying the ART script to output structured JSON data so the reconnaissance results can be automatically ingested by a Security Information and Event Management (SIEM) system.                                              Vulnerability Triage Integrating tools like Nuclei or linking discovered service versions to directly known CVE identifiers to provide automatic risk scoring in the report.                                                                               
Finally I want to express my sincere thanks for the structure of this cybersecurity project. The progression from Red Team tasks to Blue Team analysis and culminating in a full automation project provided a robust and highly practical education. It has given me not just theoretical knowledge but tangible executable skills that I am confident will form the bedrock of my future career in cybersecurity.                                                                             














































"""

if __name__ == "__main__":
    create_translated_pdf(translated_text)