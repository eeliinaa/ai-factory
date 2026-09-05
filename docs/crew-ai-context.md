# CrewAI konteksts

## Mērķis
- Šis ir globālais projekta konteksta fails.
- Tā mērķis ir uzturēt vienā vietā stabilos projekta noteikumus, svarīgākos lēmumus, pieņēmumus un stratēģisko virzienu.
- Šis fails nav pilnā projekta specifikācija.
- Detalizētā specifikācija dzīvo failā `mix/context/AI_PRODUCT_FACTORY_PROJECT_SPEC.md`.
- Ja starp šo failu un specifikācijas failu rodas pretruna, par avotu jāuzskata specifikācijas fails.

## Struktūras lēmums
- Repozitorijs: `elina-birite/iso`
- Globālais konteksta fails: `mix/context/crew-ai-context`
- Galvenais specifikācijas fails: `mix/context/AI_PRODUCT_FACTORY_PROJECT_SPEC.md`
- Projektā paredzēti tikai divi galvenie konteksta slāņi:
  - globālais projekta konteksts,
  - aktīvais tematiskais konteksts konkrētam virzienam vai tēmai.
- Katram jaunam tematiskajam virzienam vēlāk var tikt veidots atsevišķs aktīvais context fails, bet globālie noteikumi paliek šajā dokumentā.

## Projekta virziens
- Projekta mērķis ir izveidot lean AI-assisted sistēmu, kas no augsta līmeņa tēmas nonāk līdz publicēšanai gatavam digitālam produktam.
- Sistēmai jāiet tālāk par ideju ģenerēšanu un jānoved process līdz reāliem produkta failiem, iepakojumam un Etsy listing materiāliem.
- Primārais sākuma mērķis ir pēc iespējas ātrāk nonākt pie pirmajiem ieņēmumiem ar digitāliem produktiem.
- Agrīnā validācija un monetizācija sākotnēji fokusēta uz Etsy.
- Sākuma pieeja ir produktu portfeļa pieeja: labāk radīt vairākus pietiekami labus testējamus produktus nekā ilgi slīpēt vienu hipotētiski perfektu produktu.

## Galvenie arhitektūras principi
- Projekts tiek būvēts Python valodā.
- AI jāizmanto tikai tur, kur vajadzīga reasoning, izvērtēšana vai satura ģenerēšana.
- Deterministiskie uzdevumi jārealizē Python kodā.
- Sistēmu nevajag modelēt kā “everything is an agent”.
- Aģentu orķestrācija sākumā tiek veidota ar **CrewAI**.
- MVP posmā aģenti tiek darbināti **secīgi**, nevis paralēli.
- Paralēla izpilde ir vēlākas optimizācijas iespēja, nevis sākuma prasība.
- Arhitektūrai jābūt pārnēsājamai un tā nedrīkst būt cieši piesieta vienam LLM piegādātājam.
- LLM piekļuves slānim jābūt atdalītam no biznesa loģikas.
- **OpenAI** ir sākuma motors, nevis pastāvīga arhitektūras atkarība.

## Galvenais darba plūsmas princips
- Sistēmas ievade ir:
  - viena augsta līmeņa tēma,
  - viens aktīvais tematiskais context fails.
- Sistēmai pašai jāspēj:
  - atrast konkrētas problēmas vai apakštēmas,
  - izvērtēt iespējas,
  - izvēlēties spēcīgāko virzienu,
  - izveidot produktu,
  - sagatavot listing un preview materiālus,
  - iepakot gala rezultātu.
- Cilvēka obligātā iesaiste MVP plūsmā paredzēta tikai gala pārskatam.
- Starpposmu manuāli approval nav normāla plūsmas daļa.

## Galvenie AI lomu lēmumi
- MVP posmā prioritārās AI lomas ir:
  - **Research Agent**
  - **Evaluator Agent**
  - **Product Architect**
  - **Product Creator**
  - **QA Agent**
  - **Listing Agent**
- Nedrīkst radīt atsevišķus LLM aģentus darbiem, ko lētāk un uzticamāk var izdarīt ar kodu.

## Koda moduļi, kas jārealizē deterministiski
- Context Manager
- Budget Controller
- Technical QA
- PDF Builder / export layer
- File/folder structure builder
- ZIP / package builder
- Database write layer
- Artifact registry
- Performance metrics ingestion layer

## Produkta un MVP robežas
- Pirmais praktiskais MVP mērķis ir pilna plūsma no tēmas līdz vienam Etsy-ready digitālam produktam.
- Produkts nav uzskatāms par gatavu, ja ir tikai idejas vai konceptuāli ieteikumi.
- Minimums ir buyer-facing produkta pakete ar failiem, instrukcijām, summary, included files, benefits, listing draft un preview plānu.
- Automātiska Etsy publicēšana nav pirmā MVP daļa.
- Pilns SaaS, browser extensions, local mini-tools un sarežģīti instalējami risinājumi nav pirmā MVP prioritāte.

## Prioritārie produktu tipi
- Pirmajās iterācijās prioritāri ir:
  - `WORKSHEET_BUNDLE`
  - `TEMPLATE_BUNDLE`
  - `PDF_TOOLKIT`
  - `PROMPT_TEMPLATE_HYBRID`
- `ProductType` slānis ir obligāts arhitektūras princips.
- Produkti nedrīkst tikt apstrādāti kā viens universāls tips.
- Prompt-only produkts nav prioritārais sākuma formāts.
- Prompti labāk izmantojami kā bonuss vai daļa no hibrīdprodukta.

## Research un evaluation lēmumi
- Research jābūt **evidence-first**, nevis tikai brīvai ideju ģenerēšanai.
- Pirms izvēles jāapkopo strukturēti signāli par pieprasījumu, konkurenci, cenu diapazonu, dominējošajiem formātiem, gaps, izveides ātrumu un series potential.
- Kandidātu izvērtēšanai jābūt balstītai strukturētā scoring modelī, nevis vienā brīvā LLM viedoklī.
- Prioritārie scoring dimensioni ir:
  - demand
  - competition / saturation
  - production speed
  - price potential
  - series potential
  - automation fit

## QA un refinement lēmumi
- QA jādala divos slāņos:
  - **AI QA** satura, skaidrības, loģikas un noderīguma pārbaudei,
  - **Technical QA** failu, struktūras, eksporta un packaging pārbaudei.
- Refinement jābūt kontrolētam.
- Maksimālais refinement ciklu skaits MVP posmā ir **2**.
- QA aktivizē uzlabošanu tikai būtisku problēmu gadījumā.
- “Pietiekami labs” rezultāts ir pieņemams, ja tas ir publicējams un saprotams.

## Storage un datu lēmumi
- Reālie artefakti glabājas failos un mapēs.
- Strukturētie lēmumi, kandidāti, score dati, atlasītie produkti, artifact metadata, listing metadata un performance dati glabājas **SQLite**.
- Garš artefaktu saturs pēc noklusējuma nav jāglabā SQLite.
- Sistēmai jāspēj uzkrāt rezultātus un vēlāk izmantot tos nākamajiem lēmumiem.

## Budget un cost-efficiency lēmumi
- Sistēmai jābūt budget-aware.
- AI/API izmaksas jāseko pa posmiem, ne tikai kopā.
- Jābūt skaidriem stop nosacījumiem, lai sistēma netērē budžetu vājiem vai iestrēgušiem runiem.
- Jāpreferē:
  - mazāks un precīzāks konteksts katram solim,
  - template-first pieeja,
  - structured outputs starpposmos,
  - deterministic code tur, kur tas ir iespējams,
  - cached rezultātu un intermediate outputu reuse,
  - preview ģenerēšana tikai pēc pietiekama QA sliekšņa.
- Sistēma jāoptimizē nevis tikai uz lētu vienu run, bet uz labu **cost per publishable product**.

## Pašreizējais stratēģiskais virziens
- Projekts orientēts uz problem-first digitāliem produktiem.
- Prioritāte ir skaidras, praktiskas un monetizējamas problēmas.
- Priekšroka dodama problēmām, kas palīdz pircējam:
  - ietaupīt laiku,
  - iegūt skaidrību,
  - samazināt kļūdas,
  - sakārtot procesu,
  - ātrāk nonākt pie rezultāta vai ieņēmumiem.
- AI nevajag likt priekšplānā, ja produkts labāk pārdodas kā praktisks workflow vai business produkts.

## Pašreizējās auditorijas un tēmu hipotēzes
- Šobrīd perspektīvi virzieni ir:
  - profesionālo darba plūsmu produkti,
  - side-hustleru un digitālo produktu veidotāju produkti,
  - Etsy pārdevēju atbalsta produkti.
- Tēma ir stiprāka, ja:
  - problēma ir skaidri atpazīstama,
  - produkts ir ātri iepakojams,
  - value proposition ir skaidrs,
  - ir iespējams radīt vairāk nekā vienu produktu vienā virzienā,
  - nav vajadzīga smaga tehniska implementācija pirmajam publicējamajam rezultātam.

## Uzturēšanas noteikums
- Šim failam jāpaliek īsam un stabilam.
- Šeit jāglabā tikai globālie noteikumi, svarīgākie lēmumi, pieņēmumi un pašreizējais stratēģiskais virziens.
- Detalizētas specifikācijas, tabulu lauki, scoring svari, output folder struktūras un citi implementation-level noteikumi jāuztur specifikācijas failā.
- Ja kāda ideja, hipotēze vai nišas izvēle kļūst pārāk detalizēta, tai jādzīvo atsevišķā tematiskajā context failā, nevis šeit.
