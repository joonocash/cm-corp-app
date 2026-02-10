# Projektrapport — CM Corp Webinar Signup

---

# Uppgift 1 — Utvecklingsprocess och arbetsmetodik

## 1. Introduktion

### Syfte
Syftet med denna projektdokumentation är att beskriva och reflektera över hur utvecklingsarbetet av webbapplikationen CM Corp Webinar Signup har organiserats, genomförts och levererats. Dokumentet belyser de verktyg, metoder och arbetsflöden som använts, med fokus på att visa förståelse för hur de samverkar i en modern utvecklingsprocess.

### Projektets omfattning
Projektet har bestått av att utveckla en webbapplikation för CM Corp — ett fiktivt företag som anordnar professionella webinarier. Applikationen låter besökare registrera sig för kommande webinarier via ett formulär och ger administratörer möjlighet att hantera anmälningar via en skyddad admin-panel.

Huvudfunktionalitet:
- **Publik signup-sida** — Formulär för att registrera sig till webinarier med fält för namn, jobbtitel, företag, e-post och samtycke.
- **Admin-panel** — Lösenordsskyddad vy som visar alla anmälningar, med sök, CSV-export och raderingsmöjlighet.
- **Inloggningssystem** — Session-baserad autentisering för admin-sidan.
- **CI/CD-pipeline** — Automatiserad bygge och driftsättning via GitHub Actions till Azure Container Apps.

### Målgrupp
Dokumentet riktar sig till kursledare och examinatorer, men även till teammedlemmar och framtida utvecklare som behöver förstå projektets uppbyggnad och arbetssätt.

---

## 2. Den inre utvecklingsloopen

### Jira och backlog-hantering
Produktbackloggen har hanterats i Jira, där alla funktionskrav och tekniska uppgifter har dokumenterats som issues. Arbetsflödet har följt en typisk Kanban/Scrum-modell:

1. **Product Backlog** — Alla önskade funktioner och förbättringar samlas här, prioriterade efter affärsvärde.
2. **Sprint Backlog** — Inför varje sprint väljs de högst prioriterade items ut baserat på teamets kapacitet.
3. **In Progress** — Utvecklaren tar ett item, skapar en feature branch och börjar arbeta.
4. **Code Review** — En pull request skapas och granskas av en annan teammedlem.
5. **Done** — Efter godkänd granskning och merge till main markeras uppgiften som klar.

En arbetsuppgift tar sig alltså från idé (backlog item) genom sprintplanering, kodning, granskning och slutligen leverans till produktion via CI/CD-pipelinen.

### Versionshantering med Git och GitHub
Projektet har använt Git som versionshanteringssystem med GitHub som fjärrrepository (joonocash/cm-corp-app).

**Branching-strategi:**
- `main` — Stabil produktionsbranch. All kod som hamnar här deployeras automatiskt till Azure.
- `feature/*` — Feature branches skapas från main för varje ny funktionalitet eller buggfix.
- Commits kopplas till Jira-items genom att inkludera issue-nyckeln i commit-meddelanden (t.ex. "CM-12: Add admin login").
- Pull requests används för kodgranskning innan merge till main.

**Exempel på arbetsflöde:**
```
git checkout -b feature/admin-login
# ... utveckling ...
git add app/presentation/routes/admin_routes.py
git commit -m "CM-15: Add admin login with session-based auth"
git push -u origin feature/admin-login
# → Skapa pull request på GitHub
# → Kodgranskning
# → Merge till main
# → Automatisk deploy via GitHub Actions
```

### Utvecklingsmiljön
VS Code har varit det primära utvecklingsverktyget med följande uppsättning:
- **Python-extension** — IntelliSense, linting och debugging för Flask-applikationen.
- **Git-integration** — Inbyggd visualisering av ändringar, staging och commits direkt i editorn.
- **Terminal** — Integrerad terminal för att köra Flask-servern, Git-kommandon och Docker-byggen.
- **Live Preview** — Snabb feedback-loop genom att köra `python run.py` och se ändringar i realtid.

Utvecklingsmiljön har körts i Google IDX (molnbaserad Nix-miljö) med Python 3.11 och en virtuell miljö (.venv) för pakethantering.

### Kopplingen Jira–GitHub
Integrationen mellan Jira och GitHub har möjliggjort spårbarhet genom hela utvecklingsprocessen. Genom att referera till Jira-nycklar i commits och pull requests kan man:
- Se vilken kod som hör till vilken uppgift.
- Automatiskt uppdatera Jira-status när en PR mergas.
- Få en komplett historik över hur varje krav har implementerats.

Denna koppling är värdefull eftersom den skapar transparens för hela teamet och gör det enkelt att förstå varför en viss kodändring gjordes.

---

## 3. Arbetsmetodik och sprintarbete

### 3.1 Sprintplanering och genomförande
Sprintarna har organiserats i tvåveckors cykler med följande struktur:

- **Sprint Planning** — I början av varje sprint prioriteras och väljs items från produktbackloggen. Teamet diskuterar scope och uppskattningar.
- **Daily Standup** — Kort daglig avstämning om vad som gjorts, vad som planeras och eventuella blockerare.
- **Sprint Review/Demo** — I slutet av sprinten demonstreras den levererade funktionaliteten.
- **Sprint Retrospective** — Reflektion över vad som fungerat bra och vad som kan förbättras.

Arbetsinsatsen har uppskattats med story points baserade på komplexitet snarare än tid. Initialt var uppskattningarna osäkra — exempelvis underskattades refaktoreringen till trelagrarsarkitektur som visade sig vara mer komplex än förväntat. Över tid blev uppskattningarna bättre i takt med att teamet fick bättre förståelse för kodbas och verktyg.

### 3.2 User stories
User stories har använts för att säkerställa att utvecklingen alltid utgår från användarens behov. Format:
*"Som [roll] vill jag [funktion] så att [nytta]."*

**Konkret exempel — Admin-inloggning:**

> *"Som administratör vill jag kunna logga in med lösenord för att skydda admin-panelen från obehöriga."*

**Implementering:**
1. Skapade en `login_required`-decorator i `admin_routes.py` som kontrollerar session-status.
2. Byggde en inloggningssida (`admin_login.html`) med formulär för användarnamn och lösenord.
3. Implementerade login/logout-routes i admin-blueprinten.
4. Flyttade autentiseringsuppgifterna till miljövariabler (via `config.py` och `.env`) för att inte exponera lösenord i koden.

Acceptanskriterier:
- Admin-sidan kräver inloggning — ej inloggade omdirigeras till login.
- Felaktiga uppgifter visar felmeddelande.
- Logout rensar sessionen och omdirigerar till startsidan.

Alla kriterier uppfylldes och verifierades manuellt.

### 3.3 Pull requests och kodgranskning
Pull requests har använts som en kvalitetsgrind innan kod mergas till main.

**Process:**
1. Utvecklaren skapar en PR med beskrivning av ändringen.
2. En granskare läser igenom koden och lämnar kommentarer.
3. Eventuella ändringar görs baserat på feedback.
4. PR godkänns och mergas.

**Vad kodgranskningen har tillfört:**
- Fångat potentiella säkerhetsproblem, t.ex. att admin-lösenord hårdkodades direkt i källkoden — detta ledde till att uppgifterna flyttades till miljövariabler.
- Identifierat CSS-buggar som att logotypen renderades helt vit på grund av ett felaktigt bildfilter.
- Förbättrat kodkvalitet genom att påpeka möjligheter till förenkling och bättre namngivning.

### 3.4 Demo och återkoppling
Demos har genomförts i slutet av varje sprint där teamet visar den nya funktionaliteten live i webbläsaren.

**Exempel på feedback som påverkat arbetet:**
- Under en demo påpekades att bakgrundsgradienterna "bröts" vid scrollning, vilket ledde till att `background-attachment: fixed` implementerades i CSS.
- Feedback om att "About this webinar"-sektionen borde beskriva CM Corp som företag resulterade i en omskrivning av innehållet till "About CM Corp".
- Önskemål om att integrera CM Corp-logotypen i headern ledde till att logotypen lades till som bild i navigationen.

---

## 4. Reflektion

### Utmaningar
- **Miljöhantering** — Att arbeta i en Nix-baserad molnmiljö (Google IDX) innebar utmaningar med pakethantering. Systemets Python var "externally managed" vilket krävde att all installation skedde i en virtuell miljö.
- **Arkitekturbeslut** — Att refaktorera en monolitisk `app.py` till en trelagrarsarkitektur med Blueprints och Application Factory var mer komplext än förväntat, särskilt att få alla sökvägar för templates och statiska filer rätt.
- **CI/CD-konfiguration** — Att sätta upp OIDC-federation mellan GitHub och Azure krävde flera steg med Azure CLI som var svåra att felsöka.
- **Agilt i praktiken** — Det var ibland svårt att bryta ner stora uppgifter i tillräckligt små stories. Refaktoreringen var svår att leverera inkrementellt utan att bryta befintlig funktionalitet.

### Lärdomar
- **Planera arkitekturen tidigt** — Att börja med en genomtänkt struktur sparar mycket refaktoreringsarbete senare.
- **Automatisera tidigt** — CI/CD-pipelinen bör sättas upp så tidigt som möjligt. Det skapar trygghet att kunna deploya med ett knapptryck.
- **Små commits och PR:er** — Mindre ändringar är lättare att granska och minskar risken för konflikter.
- **Miljövariabler för allt känsligt** — Aldrig hårdkoda lösenord, nycklar eller annan känslig information i källkoden.

### AI som verktyg
AI-verktyg (Claude Code) har haft en betydande inverkan på arbetssättet under kursen:

**Vad AI har hjälpt med:**
- Snabb scaffolding av projektstruktur och boilerplate-kod.
- Refaktorering av monolitisk kod till trelagrarsarkitektur.
- Generering av CSS och JavaScript med konsistent stil.
- Felsökning av konfigurationsproblem (Docker, Azure, GitHub Actions).
- Att förklara koncept som OIDC-federation och Application Factory-mönstret.

**Var egen förståelse fortfarande behövts:**
- Att förstå *varför* arkitekturen ser ut som den gör — AI kan generera kod, men utvecklaren måste förstå designbesluten.
- Att bedöma säkerhet — AI-genererad kod kan innehålla subtila problem (som CSS-filtret som gjorde logotypen osynlig).
- Att prioritera och planera — AI kan inte avgöra vad som är viktigast för affären.
- Att granska och validera — all AI-genererad kod måste förstås och verifieras av utvecklaren.

AI har alltså fungerat som en kraftfull accelerator, men kräver att utvecklaren har tillräcklig kunskap för att styra, granska och förstå det som produceras.

---

## 5. Slutsats

Projektsetupen med Git/GitHub, Jira, sprintbaserat arbete och en automatiserad CI/CD-pipeline har skapat ett effektivt och strukturerat arbetssätt. Genom att kombinera agila metoder med moderna verktyg har teamet kunnat leverera fungerande funktionalitet i korta cykler med kontinuerlig feedback.

**Utvecklade färdigheter som är relevanta för rollen som IT-projektledare:**
- **Förmåga att planera och bryta ner arbete** — Att använda user stories och sprintplanering för att styra utvecklingen.
- **Förståelse för DevOps** — Insikt i hur CI/CD, containerisering och molntjänster hänger ihop.
- **Teknisk kommunikation** — Att kunna beskriva arkitektur och tekniska val för både utvecklare och stakeholders.
- **Kvalitetssäkring** — Förståelse för kodgranskning, testning och säkerhetstänk i utvecklingsprocessen.
- **Riskhantering** — Att identifiera och hantera tekniska utmaningar tidigt, som miljöproblem och säkerhetsfrågor.

---
---

# Uppgift 2 — Software Design Description (SDD)

## 1. Introduktion

### Syfte
Webbapplikationen CM Corp Webinar Signup är en registreringsplattform för professionella webinarier. Syftet är att låta besökare enkelt anmäla sig till kommande event och att ge administratörer en översikt över alla anmälningar.

### Omfattning
Systemets huvudfunktioner:
- **Registreringsformulär** — Publikt formulär med validering av e-post och samtycke.
- **Admin-panel** — Lösenordsskyddad vy med tabell över alla anmälningar, sökfunktion, CSV-export och raderingsmöjlighet.
- **Autentisering** — Session-baserad inloggning för admin-sidan.
- **Responsiv design** — Modern, mörk UI som fungerar på desktop och mobil.
- **Automatiserad deploy** — CI/CD-pipeline som bygger och driftsätter vid push till main.

### Teknologistack

| Teknologi | Användning |
|---|---|
| **Python 3.11** | Programmeringsspråk |
| **Flask 3.0** | Webbramverk |
| **Gunicorn 21.2** | WSGI-server för produktion |
| **HTML/CSS/JavaScript** | Frontend |
| **localStorage** | Klientbaserad datalagring |
| **Docker** | Containerisering |
| **GitHub Actions** | CI/CD-pipeline |
| **Azure Container Registry** | Container image-lagring |
| **Azure Container Apps** | Hosting/driftsättning |

---

## 2. Applikationens arkitektur

### Högnivå-beskrivning
Applikationen följer en **trelagrarsarkitektur** (Three-Tier Architecture) som separerar ansvar i tre distinkta lager:

```
┌─────────────────────────────────────────────────┐
│              PRESENTATIONSLAGER                  │
│  (Templates, CSS, JavaScript, Routes/Blueprints) │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ index.html│  │ admin.html│  │ admin_login   │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│  ┌──────────┐  ┌───────────┐                     │
│  │style.css │  │ app.js    │                     │
│  │admin.css │  │ admin.js  │                     │
│  └──────────┘  └───────────┘                     │
│  ┌─────────────────┐  ┌──────────────────┐       │
│  │ main_routes.py  │  │ admin_routes.py  │       │
│  │ (Blueprint)     │  │ (Blueprint)      │       │
│  └─────────────────┘  └──────────────────┘       │
├─────────────────────────────────────────────────┤
│              AFFÄRSLOGIKLAGER                     │
│         (Services, validering, regler)            │
│                                                   │
│  ┌──────────────────────────────────────┐        │
│  │        webinar_service.py            │        │
│  │  - validate_signup_data()            │        │
│  │  - process_signup()                  │        │
│  │  - get_webinar_config()              │        │
│  └──────────────────────────────────────┘        │
├─────────────────────────────────────────────────┤
│             DATAÅTKOMSTLAGER                     │
│        (Modeller, Repositories)                   │
│                                                   │
│  ┌────────────────┐  ┌──────────────────────┐    │
│  │  signup.py      │  │ signup_repository.py │    │
│  │  (Dataclass)    │  │ (CRUD-operationer)   │    │
│  └────────────────┘  └──────────────────────┘    │
├─────────────────────────────────────────────────┤
│              DATALAGRING                          │
│        (localStorage i webbläsaren)               │
│        (Framtida: SQLite / Azure SQL)             │
└─────────────────────────────────────────────────┘
```

### De olika lagren och hur de samverkar

**Presentationslagret** hanterar allt som användaren ser och interagerar med — HTML-templates, CSS-styling, JavaScript-logik och Flask-routes. Routes tar emot HTTP-förfrågningar och delegerar till affärslogiklagret.

**Affärslogiklagret** innehåller applikationens regler och logik — validering av e-post, kontroll av samtycke, och konfigurationshantering. Det fungerar som en mellanhand mellan presentation och data.

**Dataåtkomstlagret** definierar datamodeller och tillhandahåller ett abstrakt interface för att spara och hämta data. I nuläget är lagringen klientbaserad (localStorage), men repositoryklassen är förberedd för framtida databasintegration.

### Flask Blueprints och Application Factory

**Application Factory** (`app/__init__.py`) är ett mönster där Flask-applikationen skapas via en funktion (`create_app()`) istället för som en global variabel. Fördelar:
- Möjliggör olika konfigurationer (development, production, testing).
- Underlättar testning genom att skapa isolerade app-instanser.
- Krävs för att Gunicorn ska kunna starta applikationen korrekt.

**Blueprints** organiserar routes i moduler:
- `main` — Hanterar den publika sidan (`/`) och API-endpoint (`/api/signup`).
- `admin` — Hanterar admin-panelen (`/admin/`), login (`/admin/login`) och logout (`/admin/logout`).

### Kodexempel — Affärslogiklagret

Här visas ett utdrag ur `webinar_service.py` som illustrerar hur affärslogiklagret validerar signup-data:

```python
class WebinarService:
    def __init__(self, config=None):
        self.repository = SignupRepository()
        self.config = config or {}

    def validate_signup_data(self, data: dict) -> Tuple[bool, str]:
        email = data.get('email', '').strip()
        consent = data.get('consent', False)

        if not email:
            return False, "Please enter your email."

        if not SignupData.is_valid_email(email):
            return False, "That email doesn't look quite right."

        if not consent:
            return False, "Please tick the consent box to sign up."

        return True, ""

    def process_signup(self, data: dict) -> Dict[str, Any]:
        is_valid, error_msg = self.validate_signup_data(data)
        if not is_valid:
            return {'success': False, 'error': error_msg}

        signup = SignupData(
            email=data.get('email', '').strip(),
            consent=data.get('consent', False),
            first_name=data.get('firstName', '').strip() or None,
            last_name=data.get('lastName', '').strip() or None
        )

        success = self.repository.save(signup)
        if success:
            return {'success': True, 'message': "You're signed up!"}
        else:
            return {'success': False, 'error': "Something went wrong."}
```

**Förklaring:** Metoden `validate_signup_data()` kontrollerar att e-post finns och har korrekt format, samt att användaren gett samtycke. Om valideringen lyckas skapar `process_signup()` ett `SignupData`-objekt och sparar det via repositoryt. Servicen vet inte *hur* data sparas — det är repositoryts ansvar. Denna separation gör att vi enkelt kan byta ut localStorage mot en riktig databas utan att ändra affärslogiken.

---

## 3. Databashantering

### Nuvarande implementation
I nuläget använder applikationen **localStorage** i webbläsaren för att lagra anmälningar. All data sparas och läses via JavaScript på klientsidan med nyckeln `webinar_signups_v1`. Detta innebär att data är bunden till den specifika webbläsaren och enheten.

### Datamodellen
Trots avsaknaden av en traditionell databas har en datamodell definierats med Python-dataclasses:

```python
@dataclass
class SignupData:
    email: str
    consent: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
```

Denna modell definierar strukturen på signup-data med validering och serialisering (till/från JSON och CSV).

### Förberedelse för framtida databasintegration
Repository-mönstret (`signup_repository.py`) tillhandahåller ett interface med metoder som `save()`, `get_all()`, `get_by_email()` och `count()`. Dessa är för närvarande no-ops men är förberedda för att implementeras med SQLAlchemy:

```python
class SignupRepository:
    def save(self, signup: SignupData) -> bool:
        # TODO: Implement database insert
        # db.session.add(signup)
        # db.session.commit()
        return True

    def get_all(self) -> List[SignupData]:
        # TODO: Query database
        return []
```

Vid en framtida migration till t.ex. SQLite (utveckling) eller Azure SQL (produktion) behöver man:
1. Definiera SQLAlchemy-modeller baserade på den befintliga dataclassen.
2. Implementera repository-metoderna med databasanrop.
3. Använda migreringsverktyg som Flask-Migrate/Alembic för att hantera schemaändringar.

### Autentisering
Admin-autentisering implementeras via Flask-sessioner. Administratörens inloggningsuppgifter läses från miljövariabler (`ADMIN_USERNAME`, `ADMIN_PASSWORD`) via `config.py`. I produktionsmiljö sätts dessa som miljövariabler på Azure Container Apps, vilket innebär att de aldrig exponeras i källkoden.

---

## 4. Från lokal utveckling till produktion — Everything as Code

### Applikationskoden
All Python/Flask-kod versionshanteras i Git och ligger i GitHub-repositoryt `joonocash/cm-corp-app`. Varje ändring spåras med commits och granskas via pull requests.

### Containerisering
Applikationen paketeras som en Docker-container:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
```

**Förklaring:**
- Utgår från en minimal Python 3.11-image.
- Installerar beroenden från `requirements.txt`.
- Kopierar in applikationskoden.
- Startar Gunicorn som WSGI-server med Application Factory-anropet `app:create_app()`.

Observera att Gunicorn används istället för Flasks inbyggda utvecklingsserver, eftersom den är designad för produktionsbelastning med stöd för flera workers.

### CI/CD-pipeline
GitHub Actions-workflowen (`deploy.yml`) definierar hela bygge- och deployprocessen som kod. Vid varje push till `main` körs pipelinen automatiskt.

### Miljökonfiguration
Miljövariabler styr applikationens beteende:
- **Lokalt** — `.env`-fil med utvecklingsvärden (läses via `python-dotenv`).
- **Produktion (Azure)** — Miljövariabler sätts direkt på Azure Container Apps.

Exempel på skillnader:

| Variabel | Lokal utveckling | Azure-produktion |
|---|---|---|
| `FLASK_ENV` | development | production |
| `SECRET_KEY` | dev-secret-key... | Kryptografiskt slumpad nyckel |
| `DEBUG` | True | False |
| `SESSION_COOKIE_SECURE` | False | True |

### Varför "Everything as Code" är värdefullt ur ett projektledarperspektiv
- **Reproducerbarhet** — Hela miljön kan återskapas från koden, inget "det fungerade på min maskin".
- **Spårbarhet** — Alla ändringar loggas i Git, inklusive infrastruktur och pipeline.
- **Samarbete** — Alla i teamet arbetar med samma uppsättning, definierad i kod.
- **Automatisering** — Minskar manuella fel och frigör tid från repetitiva uppgifter.
- **Onboarding** — Nya teammedlemmar kan snabbt komma igång genom att klona repot.

---

## 5. CI/CD-pipeline och driftsättning

### Leveranskedjan

```
┌──────────┐    ┌──────────────┐    ┌──────────┐    ┌─────────────────┐
│  GitHub   │───▶│ Docker-bygge │───▶│   ACR    │───▶│ Container Apps  │
│  (Push)   │    │ (Image)      │    │ (Lagring)│    │ (Driftsättning) │
└──────────┘    └──────────────┘    └──────────┘    └─────────────────┘
```

**Steg för steg:**

1. **GitHub** — Utvecklaren pushar kod till `main`-branchen. GitHub Actions triggas automatiskt.
2. **Docker-bygge** — Azure Container Registry bygger en Docker-image direkt från repositoryt med `az acr build`.
3. **Azure Container Registry (ACR)** — Den byggda imagen taggas med commit-SHA:t och lagras i registret.
4. **Azure Container Apps** — Container Apps uppdateras med den nya imagen via `az containerapp update`.
5. **Verifiering** — Pipelinen gör en HTTP-healthcheck mot den deployade applikationen och verifierar att den svarar med HTTP 200.

### OIDC-federation för lösenordsfri autentisering
Istället för att lagra Azure-credentials (användarnamn/lösenord) som GitHub Secrets används **OpenID Connect (OIDC) federation**:

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

**Varför detta är bättre:**
- **Inga lagrade lösenord** — Inget lösenord kan läcka eller behöva roteras.
- **Kortlivade tokens** — Varje pipeline-körning får en tillfällig token som upphör automatiskt.
- **Minsta behörighet** — Managed Identity ges bara de roller den behöver (AcrPush, Contributor).
- **Ingen manuell hantering** — Ingen behöver komma ihåg att förnya credentials.

### Kodexempel — GitHub Actions Workflow

Här visas deploy-steget i `deploy.yml`:

```yaml
- name: Build and push to ACR
  run: |
    az acr build \
      --registry ${{ vars.ACR_NAME }} \
      --image cm-corp-app:${{ github.sha }} .
```

**Förklaring:** Kommandot `az acr build` skickar hela projektets kontext till Azure Container Registry, som bygger Docker-imagen i molnet. Imagen taggas med `${{ github.sha }}` — det unika commit-ID:t — vilket säkerställer att varje deploy kan spåras tillbaka till exakt den version av koden som byggdes.

```yaml
- name: Verify deployment
  run: |
    FQDN=$(az containerapp show \
      --name ${{ vars.CONTAINER_APP }} \
      --resource-group ${{ vars.RESOURCE_GROUP }} \
      --query "properties.configuration.ingress.fqdn" -o tsv)
    for i in 1 2 3 4 5; do
      HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$FQDN")
      if [ "$HTTP_CODE" = "200" ]; then
        echo "Health check passed!"
        exit 0
      fi
      sleep 10
    done
    echo "Health check failed!" && exit 1
```

**Förklaring:** Efter deploy hämtas applikationens publika URL (FQDN) från Azure. Sedan görs upp till 5 försök att nå applikationen via HTTP. Om den svarar med statuskod 200 anses deployen lyckad. Om den inte svarar inom 50 sekunder markeras pipelinen som misslyckad, vilket ger omedelbar varning om att något gått fel.

---

## 6. Slutsats och framtida förbättringar

### Styrkor i designen
- **Tydlig separation** — Trelagrarsarkitekturen gör koden organiserad och lätt att navigera.
- **Framtidssäkrad** — Repository-mönstret och Application Factory gör det enkelt att lägga till databas, tester och nya endpoints.
- **Automatiserad leverans** — CI/CD-pipelinen säkerställer att varje push till main automatiskt bygger, deployar och verifierar applikationen.
- **Säkerhetstänk** — Känsliga uppgifter lagras som miljövariabler, sessions är korrekt konfigurerade, och OIDC används för lösenordsfri deploy.

### Möjliga förbättringar

| Förbättring | Beskrivning |
|---|---|
| **Databas-integration** | Byta från localStorage till Azure Table Storage eller Azure SQL för persistent, serverbaserad lagring. |
| **Automatiserade tester** | Lägga till enhetstester (pytest) och integrationstester i CI/CD-pipelinen. |
| **HTTPS och custom domain** | Konfigurera ett eget domännamn med SSL-certifikat. |
| **Rate limiting** | Skydda signup-endpointen mot missbruk med Flask-Limiter. |
| **E-postbekräftelse** | Skicka bekräftelsemail vid registrering via SendGrid eller liknande tjänst. |
| **Rollbaserad åtkomst** | Utöka autentiseringen med flera roller och mer granulär behörighetskontroll. |
| **Monitoring och logging** | Integrera Application Insights för att övervaka applikationens hälsa och prestanda i produktion. |
| **Staging-miljö** | Lägga till en staging-miljö i CI/CD-pipelinen för att testa innan produktion. |

Sammanfattningsvis har projektet levererat en fungerande, välstrukturerad webbapplikation med en modern utvecklings- och leveranskedja. Arkitekturen är förberedd för att växa med framtida krav, och arbetsmetodiken har gett värdefull erfarenhet av att arbeta agilt med DevOps-verktyg — färdigheter som är direkt applicerbara i rollen som IT-projektledare.
