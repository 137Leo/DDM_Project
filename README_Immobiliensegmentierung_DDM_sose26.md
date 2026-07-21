# Immobiliensegmentierung in King County

## Projektüberblick

Dieses Projekt untersucht, wie sich Immobilien im **King County, Washington**, anhand ihrer Lage, ihres Umfelds und ihrer baulichen Eigenschaften in nachvollziehbare Immobiliensegmente einteilen lassen.

Ausgangspunkt ist eine praktische Marketingfrage: Immobilienangebote unterscheiden sich nicht nur im Preis, sondern auch in ihrer Lage, der Qualität des Umfelds, der Größe und der Ausstattung. Eine rein objektbezogene Betrachtung erschwert es, Angebote konsistent zu positionieren und Zielgruppen passend anzusprechen. Deshalb werden Immobilien mit ähnlichen Merkmalen mithilfe von Clustering-Verfahren zu Gruppen zusammengefasst.

Die Analyse verfolgt zwei Perspektiven:

1. **Lagesegmentierung:** Identifikation räumlich und strukturell ähnlicher Nachbarschaften.
2. **Preissegmentierung:** Untersuchung, ob sich anhand von Lage- und Qualitätsmerkmalen klar unterscheidbare Preissegmente bilden lassen, obwohl der Preis nicht als Eingangsvariable verwendet wird.

Der Schwerpunkt der finalen Bewertung liegt auf der **Lagesegmentierung mit HDBSCAN**. Die Preissegmentierung ergänzt die Analyse und zeigt, wie sich die gefundenen Strukturen für die Positionierung und Bewertung von Immobilienangeboten nutzen lassen.

---

## Zielsetzung

Ziel ist es, aus heterogenen Immobiliendaten verständliche Segmente abzuleiten, die:

- Immobilien mit ähnlichen Lage- und Strukturmerkmalen zusammenfassen,
- Unterschiede zwischen Nachbarschaften sichtbar machen,
- eine konsistente Positionierung von Immobilienangeboten unterstützen,
- regionale Schwerpunkte für Marketingmaßnahmen liefern,
- besonders günstige Angebote im Vergleich zu ähnlichen Immobilien identifizieren.

Die Cluster sind **keine vorgegebenen Kategorien**, sondern werden datenbasiert aus den Ähnlichkeiten der Immobilien gebildet.

---

## Datengrundlage

### King County House Sales

Der Ausgangsdatensatz enthält:

- **21.613 Immobilienverkäufe**
- **21 ursprüngliche Merkmale**
- keine fehlenden Werte

Wichtige Ausgangsvariablen sind unter anderem:

| Variable | Bedeutung |
|---|---|
| `price` | Verkaufspreis der Immobilie |
| `sqft_living` | Wohnfläche in Square Feet |
| `sqft_lot` | Grundstücksfläche |
| `bedrooms` | Anzahl der Schlafzimmer |
| `bathrooms` | Anzahl der Badezimmer |
| `floors` | Anzahl der Etagen |
| `grade` | Bewertung der Bau- und Ausstattungsqualität |
| `condition` | Zustand der Immobilie |
| `view` | Qualität der Aussicht |
| `waterfront` | Lage am Wasser, binär codiert |
| `yr_built` | Baujahr |
| `yr_renovated` | Renovierungsjahr |
| `lat`, `long` | geografische Koordinaten |
| `zipcode` | Postleitzahl |
| `sqft_living15` | durchschnittliche Wohnfläche vergleichbarer Objekte im Umfeld |
| `sqft_lot15` | durchschnittliche Grundstücksfläche im Umfeld |

Für einen Teil der Modellierung wurde der Datensatz auf **21.436 eindeutige Häuser** reduziert, sodass pro Immobilie nur ein Verkauf berücksichtigt wird.

### Externe Datenquellen

Zur besseren Abbildung der Nachbarschaft wurden zusätzliche Informationen ergänzt:

- **Medianes Haushaltseinkommen je Postleitzahl**  
  Quelle: U.S. Census Bureau, American Community Survey (ACS)
- **Schulqualität je Bezirk**  
  Quelle: Washington Office of Superintendent of Public Instruction, OSPI Report Card
- **Distanz zum nächsten größeren ÖPNV-Knotenpunkt**

Diese Variablen erweitern die reine Objektperspektive um wirtschaftliche und infrastrukturelle Merkmale des Umfelds.

---

## Vorgehensmodell

Das Projekt wurde in vier aufeinander aufbauenden Phasen durchgeführt:

1. **Data Understanding:** Struktur, Qualität und Verteilungen der Daten verstehen.
2. **Data Preparation:** Daten bereinigen, transformieren und durch neue Merkmale ergänzen.
3. **Modellierung:** Mehrere Clustering-Verfahren auf vergleichbare Feature-Sets anwenden.
4. **Evaluation:** Modelle anhand statistischer Kennzahlen und ihrer fachlichen Interpretierbarkeit vergleichen.

---

## 1. Data Understanding

### Initial Data Analysis

Die erste Datenprüfung zeigte:

- Der Datensatz ist vollständig und enthält keine fehlenden Werte.
- `price`, `sqft_living` und `sqft_lot` sind deutlich rechtsschief verteilt.
- Die Variablen besitzen sehr unterschiedliche Größenordnungen.
- Ein auffälliger Ausreißer mit `bedrooms = 33` wurde identifiziert.
- Wohnfläche, Qualität, Badezimmer, Aussicht und Lage stehen sichtbar mit dem Preis in Zusammenhang.

### Explorative Ergebnisse

Die explorative Analyse lieferte mehrere zentrale Hinweise:

- Größere Wohnflächen gehen im Durchschnitt mit höheren Preisen einher.
- Eine höhere Qualitätsbewertung (`grade`) ist mit höheren Preisen verbunden.
- Neuere Gebäude besitzen im Mittel größere Wohnflächen als ältere Gebäude.
- Immobilien am Wasser bilden eine kleine, aber besonders hochpreisige Gruppe.
- Lage- und Nachbarschaftsmerkmale erklären wesentliche Preisunterschiede.

Für die Altersgruppen ergaben sich folgende durchschnittliche Wohnflächen:

| Altersgruppe | Durchschnittliche Wohnfläche |
|---|---:|
| Baujahr vor 1970 | 1.763 sqft |
| Baujahr 1970 bis 1990 | 2.189 sqft |
| Baujahr ab 1990 | 2.476 sqft |

Die Ergebnisse sprechen dafür, Immobilien nicht nur nach Preis oder Größe zu betrachten, sondern Lage, Umfeld und Qualität gemeinsam zu analysieren.

---

## 2. Data Preparation

### Datenbereinigung

Folgende Schritte wurden durchgeführt:

- Entfernung des Ausreißers `bedrooms = 33`
- Ausschluss rein technischer oder für die jeweilige Modellierung nicht benötigter Variablen
- Reduktion mehrfach verkaufter Immobilien auf einen Datensatz pro Haus für die Preissegmentierung
- gezielte Auswahl der Variablen für Lage- und Preissegmentmodelle

### Feature Engineering

Aus bestehenden Variablen wurden zusätzliche Merkmale abgeleitet:

| Neues Merkmal | Beschreibung |
|---|---|
| `renovated` | Gibt an, ob eine Immobilie renoviert wurde |
| `basement_available` | Gibt an, ob ein Keller vorhanden ist |
| `basement_ratio` | Anteil der Kellerfläche an der gesamten Wohnfläche |
| `age` | Alter der Immobilie zum Bezugsjahr 2015 |
| `sqft_liv_ratio` | Verhältnis der eigenen Wohnfläche zur Wohnfläche im Umfeld |
| `sqft_lot_ratio` | Verhältnis der eigenen Grundstücksfläche zur Fläche im Umfeld |
| `quality_score` | Zusammengefasster Qualitätsindikator aus mehreren standardisierten Hauseigenschaften |

Der `quality_score` reduziert mehrere ähnliche Objektmerkmale auf einen gemeinsamen Wert. Berücksichtigt werden unter anderem Schlafzimmer, Badezimmer, Etagen, Wohn- und Grundstücksfläche, relative Größenverhältnisse, `grade` und `condition`.

### Transformation und Skalierung

Die Variablen `price`, `sqft_living` und `sqft_lot` wurden mit `log1p()` logarithmisch transformiert. Dadurch werden stark rechtsschiefe Verteilungen abgeschwächt und extreme Werte dominieren die Analyse weniger stark.

Anschließend wurden numerische Variablen mit einer Z-Transformation standardisiert:

- Mittelwert = 0
- Standardabweichung = 1

Die Standardisierung ist für distanzbasierte Clustering-Verfahren wichtig, da sonst Variablen mit großen Zahlenwerten einen überproportionalen Einfluss erhalten. Binäre Merkmale wie `waterfront` wurden nicht auf die gleiche Weise skaliert.

---

## 3. Lagesegmentierung

### Verwendete Merkmale

Für die Lagesegmentierung wurden räumliche, nachbarschaftliche und strukturelle Merkmale kombiniert:

- `lat`, `long`
- `sqft_living15`
- `sqft_lot15`
- `view`
- `waterfront`
- `med_household_income`
- `distance_transit`
- `quality_score`

Damit beschreibt das Modell nicht nur den geografischen Standort, sondern auch die typische Bebauung, Erreichbarkeit, Kaufkraft und Objektqualität einer Umgebung.

### Verglichene Verfahren

#### K-Means

K-Means teilt alle Immobilien in eine vorab festgelegte Anzahl von Clustern ein. Das Verfahren erzeugt gut vergleichbare Gruppen, bildet jedoch häufig große und relativ grobe Flächen. Kleine lokale Nachbarschaften können dadurch verloren gehen.

#### DBSCAN

DBSCAN erkennt dichte Regionen und kann Ausreißer separat behandeln. Das Verfahren bildete präzisere lokale Gruppen, erzeugte jedoch viele kleine und teilweise redundante Cluster.

#### HDBSCAN

HDBSCAN erweitert den dichtebasierten Ansatz und kann unterschiedlich dichte und unterschiedlich große Cluster identifizieren. Dadurch werden kleinere Nachbarschaften erhalten, ohne den Datensatz in zu viele Einzelgruppen zu zerlegen.

### Modellvergleich

| Verfahren | Silhouette-Score | Davies-Bouldin-Index |
|---|---:|---:|
| K-Means | 0,193 | 1,415 |
| DBSCAN | 0,291 | 1,531 |
| **HDBSCAN** | **0,407** | **1,195** |

Interpretation:

- Beim **Silhouette-Score** sind höhere Werte besser.
- Beim **Davies-Bouldin-Index** sind niedrigere Werte besser.

HDBSCAN erzielt in diesem Vergleich die beste Kombination aus statistischer Trennschärfe und fachlicher Interpretierbarkeit.

### Ergebnis der Lagesegmentierung

HDBSCAN wurde als geeignetstes Verfahren ausgewählt, weil das Modell:

- geografisch präzisere Regionen als K-Means bildet,
- redundante Kleinstcluster gegenüber DBSCAN reduziert,
- kleine und große Nachbarschaften gleichzeitig abbilden kann,
- Ausreißer separat kennzeichnet,
- Unterschiede bei Einkommen, Aussicht, ÖPNV-Distanz, Lage und Qualitätsniveau sichtbar macht.

Für das Marketing entstehen damit keine künstlich gleich großen Gebiete, sondern Segmente, die den tatsächlichen lokalen Datenstrukturen besser folgen.

---

## 4. Preissegmentierung

Die zweite Modellperspektive untersucht, ob sich Immobilien anhand ihrer Lage- und Qualitätsmerkmale in unterschiedliche Preissegmente einteilen lassen. Der Verkaufspreis wurde dabei **nicht als Eingangsvariable** verwendet. Er wurde erst nach dem Clustering genutzt, um die gefundenen Gruppen anhand ihres Preisniveaus als Preissegmente zu interpretieren.

### Feature-Set

Verwendet wurden:

- `lat`, `long`
- `waterfront`
- `view`
- `condition`
- `floors`
- `median_income`
- `school_tier`

### Verglichene Verfahren

- K-Means mit `k = 4`
- hierarchisches Clustering nach Ward mit `k = 4`
- DBSCAN

### Evaluation

| Verfahren | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---|---:|---:|---:|
| **K-Means (k = 4)** | **0,239** | **1,301** | **6.173,771** |
| Hierarchisch / Ward (k = 4) | 0,219 | 1,385 | 5.573,175 |
| DBSCAN, nur Kernpunkte | 0,059 | 1,730 | 937,612 |

K-Means erreicht in dieser Modellierung bei allen drei Kennzahlen das beste Ergebnis.

### Preisbezogene Interpretation der vier Preissegmente

Die Cluster lassen sich anhand ihrer später betrachteten Preisniveaus wie folgt beschreiben:

| Segment | Typisches Preisniveau | Einordnung |
|---|---:|---|
| Budget-Segment | ca. 305.000 USD | preisorientierte Standorte und Objekte |
| Mid-Tier | ca. 510.000 USD | mittleres Preissegment |
| Premium | ca. 630.000 USD | höhere Einkommen, bessere Schul- oder Qualitätsmerkmale |
| Waterfront-Elite | ca. 1.400.000 USD | kleine exklusive Gruppe mit Wasserlage |

Ein Cluster mit **163 Immobilien** deckte sich nahezu vollständig mit den Waterfront-Objekten. Dies bestätigt, dass besondere Lageeigenschaften ein eigenständiges Preissegment kennzeichnen können.

---

## Hidden Gems

Zusätzlich wurde für jede Immobilie die Abweichung vom Medianpreis ihres eigenen K-Means-Clusters berechnet. Dadurch wird ein Objekt nicht pauschal mit allen Immobilien, sondern mit Häusern aus einer ähnlichen Lage- und Qualitätsgruppe verglichen.

Als „Hidden Gems“ wurden die günstigsten zwei Prozent innerhalb ihrer jeweiligen Peer Group betrachtet:

- **430 Immobilien** wurden als deutlich günstiger als vergleichbare Objekte identifiziert.
- Die Schwelle der unteren zwei Prozent lag bei ungefähr **52 % unter dem jeweiligen Cluster-Median**.
- Ein Extrembeispiel war ein Waterfront-Haus für 285.000 USD bei einem Cluster-Median von rund 1,4 Mio. USD.

Diese Kennzeichnung ist ein analytischer Hinweis und keine automatische Kauf- oder Investitionsempfehlung. Auffällige Objekte müssen anschließend fachlich geprüft werden, beispielsweise auf Zustand, Datenfehler, besondere Vertragsbedingungen oder andere wertrelevante Faktoren.

---

## Nutzen für das Marketing

Die Segmentierung übersetzt komplexe Immobiliendaten in verständliche Lage- und Preissegmente.

| Marketingaufgabe | Beitrag der Analyse |
|---|---|
| Positionierung von Angeboten | Immobilien können relativ zu ähnlichen Objekten beschrieben werden |
| Regionale Kampagnenplanung | Nachbarschaften mit ähnlichen Strukturen lassen sich gemeinsam ansprechen |
| Zielgruppengerechte Kommunikation | Botschaften können an Budget-, Premium- oder Waterfront-Segmente angepasst werden |
| Hervorhebung von Alleinstellungsmerkmalen | Aussicht, Wasserlage, Umfeldqualität und Erreichbarkeit werden systematisch berücksichtigt |
| Priorisierung von Angeboten | Hidden Gems können für eine vertiefte Prüfung oder Value-Kommunikation markiert werden |
| Konsistente Preisargumentation | Preisunterschiede werden mit Lage- und Qualitätsmerkmalen verbunden |

Beispiele für eine segmentbezogene Kommunikation:

- **Budget:** Preis-Leistungs-Verhältnis und Zugänglichkeit
- **Mid-Tier:** ausgewogene Kombination aus Lage, Qualität und Preis
- **Premium:** Umfeldqualität, Einkommen, Schulen und gehobene Objektmerkmale
- **Waterfront-Elite:** Exklusivität, Aussicht und besondere Lage

Die Segmentnamen dienen der Kommunikation. Sie sollten vor einem operativen Einsatz gemeinsam mit Marketing- und Immobilienexpertinnen und -experten geprüft und gegebenenfalls angepasst werden.

---

## Zentrale Erkenntnisse

1. **Lage und Nachbarschaft sind zentrale Differenzierungsmerkmale.** Einkommen, Schulumfeld, geografische Lage und Erreichbarkeit tragen wesentlich zur Segmentbildung bei.
2. **Objektqualität allein reicht nicht aus.** Erst die Kombination aus Haus-, Umfeld- und Lagemerkmalen erzeugt nachvollziehbare Preissegmente.
3. **HDBSCAN eignet sich besonders für räumliche Segmente.** Das Verfahren bildet unterschiedlich große lokale Regionen und Ausreißer besser ab als die getesteten Alternativen.
4. **K-Means eignet sich für klar kommunizierbare Preissegmente.** In der ergänzenden Preissegmentierung lieferte K-Means vier stabile und gut interpretierbare Gruppen.
5. **Preisstrukturen entstehen auch ohne Preis als Modellinput.** Die Cluster trennten sich nachträglich deutlich im Preisniveau, obwohl der Preis nicht zur Segmentbildung verwendet wurde.
6. **Peer-Group-Vergleiche schaffen zusätzlichen Nutzen.** Hidden Gems werden relativ zu ähnlichen Immobilien erkannt und nicht nur anhand eines allgemeinen Preisniveaus.

---

## Grenzen der Analyse

Die Ergebnisse sind unter folgenden Einschränkungen zu betrachten:

- Clustering ist ein exploratives, unüberwachtes Verfahren. Es gibt keine objektiv einzig richtige Segmentierung.
- Ergebnisse hängen von der Merkmalsauswahl, Skalierung und Parametrisierung ab.
- Historische Verkaufsdaten bilden nicht automatisch die heutige Preis- und Nachfragesituation ab.
- Externe Daten auf Postleitzahl- oder Bezirksebene vereinfachen Unterschiede innerhalb eines Gebiets.
- Korrelationen und Clusterzugehörigkeiten belegen keine kausalen Zusammenhänge.
- Seltene Gruppen, insbesondere Waterfront-Immobilien, können Kennzahlen und Clusterprofile stark beeinflussen.
- Hidden Gems können durch Datenfehler, Renovierungsbedarf oder nicht erfasste Merkmale entstehen.
- Die Segmente ersetzen keine individuelle Immobilienbewertung und keine fachliche Prüfung der lokalen Gegebenheiten.

---

## Empfohlene nächste Schritte

- Cluster mit lokalen Immobilienkenntnissen validieren
- verständliche, fachlich abgestimmte Segmentnamen vergeben
- Clusterprofile in Karten und Dashboards überführen
- zeitliche Stabilität der Segmente mit neueren Verkaufsdaten prüfen
- Hidden Gems durch zusätzliche Objektinformationen validieren
- Marketing-Kampagnen zunächst in ausgewählten Regionen testen
- Reaktionen und Conversion-Raten je Segment messen
- Segmentierung regelmäßig mit aktuellen Daten neu berechnen

---

## Technischer Ablauf in Kurzform

```text
Rohdaten laden
    ↓
Datenqualität und Verteilungen prüfen
    ↓
Ausreißer entfernen und Verkäufe deduplizieren
    ↓
Externe Umfeldinformationen verknüpfen
    ↓
Neue Merkmale und Qualitätsindikatoren erzeugen
    ↓
Schiefe Variablen logarithmisch transformieren
    ↓
Numerische Variablen standardisieren
    ↓
K-Means, DBSCAN, HDBSCAN und Ward-Clustering anwenden
    ↓
Modelle statistisch und fachlich bewerten
    ↓
Cluster räumlich und hinsichtlich ihres Preisniveaus interpretieren
    ↓
Lage- und Preissegmente sowie Hidden Gems ableiten
```

---

## Glossar

| Begriff | Einfache Erklärung |
|---|---|
| Cluster | Gruppe von Immobilien mit ähnlichen Merkmalen |
| Feature | Variable oder Eigenschaft, die in die Analyse eingeht |
| Standardisierung | Umrechnung von Variablen auf eine vergleichbare Skala |
| K-Means | Verfahren, das Daten in eine festgelegte Anzahl von Gruppen teilt |
| DBSCAN | Verfahren, das dichte Gruppen und Ausreißer erkennt |
| HDBSCAN | Erweiterung von DBSCAN für unterschiedlich dichte und große Gruppen |
| Silhouette-Score | Bewertet, wie klar die Cluster voneinander getrennt sind; höher ist besser |
| Davies-Bouldin-Index | Bewertet Ähnlichkeit und Streuung der Cluster; niedriger ist besser |
| Calinski-Harabasz-Score | Bewertet das Verhältnis zwischen Trennung und Streuung; höher ist besser |
| Peer Group | Vergleichsgruppe aus Immobilien mit ähnlicher Lage und Qualität |
| Hidden Gem | Immobilie, die deutlich günstiger ist als vergleichbare Objekte ihrer Peer Group |

---

## Projektteam

- Sepehr Arjmandikia
- Mayara Anastacio Matavela
- Leo Bonitz

**Studienkontext:** Data Driven Modeling, TH Köln  
**Projekt:** Immobiliensegmentierung in King County
