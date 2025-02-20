from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Définition des questions avec leurs réponses et les scores associés
questions = [
    ("Tu es dans une relation avec une femme indépendante qui gère beaucoup de choses seule. Comment réagis-tu ?", 
     [("Je la laisse tout gérer, elle est forte pour ça.", 0),
      ("Je lui propose mon aide sans m'imposer, et je prends des initiatives quand nécessaire.", 5),
      ("Je prends les commandes pour lui montrer que je suis l'homme de la situation.", 2)]),

    ("Elle traverse une période de stress intense. Que fais-tu ?", 
     [("Je la laisse tranquille, elle finira par gérer toute seule.", 0),
      ("Je l'écoute attentivement, je la soutiens émotionnellement et je l'aide si besoin.", 5),
      ("Je lui dis qu’elle exagère et qu’elle doit relativiser.", 2)]),

    ("Comment montres-tu ton engagement dans une relation ?", 
     [("Par des petits gestes quotidiens et une écoute active.", 5),
      ("En achetant des cadeaux et en la couvrant matériellement.", 2),
      ("Je ne suis pas du genre à trop montrer mes sentiments.", 0)]),

    ("Tu es en désaccord avec elle sur un sujet important. Que fais-tu ?", 
     [("J'impose mon point de vue car je pense avoir raison.", 0),
      ("Je prends le temps d'écouter son avis et on cherche un compromis.", 5),
      ("J'évite la confrontation et j'attends que ça passe.", 2)]),

    ("Elle exprime un besoin de protection et de présence. Quelle est ta réaction ?", 
     [("Je suis là quand elle en a besoin et je lui apporte du réconfort.", 5),
      ("Je pense qu’elle doit apprendre à se débrouiller seule.", 0),
      ("Je suis protecteur, mais seulement quand ça m’arrange.", 2)]),

    ("Que ressens-tu face à une femme qui réussit mieux que toi ?", 
     [("Je suis fier d’elle et je la soutiens à fond.", 5),
      ("Ça me met un peu mal à l’aise, mais j’essaie de relativiser.", 2),
      ("Je trouve cela difficile à accepter, j’ai besoin d’être au-dessus.", 0)]),

    ("Comment gères-tu une situation où elle a un problème ?", 
     [("Je cherche activement une solution avec elle.", 5),
      ("Je l’écoute et je la soutiens sans forcément intervenir.", 2),
      ("Je lui dis qu’elle doit apprendre à régler ça toute seule.", 0)]),

    ("Si elle te dit qu'elle a besoin de plus d'affection, comment réagis-tu ?", 
     [("Je fais un effort pour lui montrer mon amour au quotidien.", 5),
      ("Je lui explique que je ne suis pas très démonstratif.", 2),
      ("Je lui dis qu’elle en demande trop.", 0)]),

    ("Comment réagis-tu lorsqu'elle réussit un projet important ?", 
     [("Je célèbre avec elle et je la soutiens.", 5),
      ("Je la félicite brièvement sans trop d'enthousiasme.", 2),
      ("Je ne montre pas trop d’intérêt, ça ne me concerne pas.", 0)]),

    ("Comment abordes-tu les discussions sur l'avenir ?", 
     [("J’aime en parler et construire des projets communs.", 5),
      ("Ça me met mal à l’aise, je préfère vivre au jour le jour.", 2),
      ("Je pense que ce sont des discussions inutiles.", 0)]),

    ("Es-tu prêt à faire des efforts pour t’améliorer dans une relation ?", 
     [("Oui, l’évolution est importante.", 5),
      ("Ça dépend des efforts demandés.", 2),
      ("Non, je suis comme je suis.", 0)]),

    ("Comment réagis-tu si elle exprime ses émotions fortement ?", 
     [("Je l'écoute et je la soutiens.", 5),
      ("Je lui dis de se calmer.", 2),
      ("Je l'ignore jusqu'à ce qu'elle arrête.", 0)]),

    ("Quelle est ta priorité dans une relation ?", 
     [("L’amour et la complicité.", 5),
      ("L’équilibre et l’indépendance.", 2),
      ("Mon bien-être personnel avant tout.", 0)]),

    ("Que fais-tu si elle te reproche un manque de communication ?", 
     [("Je fais attention et j’essaie d’améliorer ça.", 5),
      ("Je lui explique que je suis comme ça.", 2),
      ("Je ne change rien, elle doit s’adapter.", 0)]),

    ("Es-tu prêt à affronter les moments difficiles ensemble ?", 
     [("Oui, on est une équipe.", 5),
      ("Ça dépend des difficultés.", 2),
      ("Je préfère éviter les conflits.", 0)])
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nom'] = request.form['nom']
        session['score'] = 0
        session['current_question'] = 0
        return redirect(url_for('quiz'))
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'current_question' not in session or session['current_question'] >= len(questions):
        return redirect(url_for('resultat'))
    
    if request.method == 'POST':
        choix = int(request.form['choix'])  # Récupérer l'index du choix sélectionné
        session['score'] += questions[session['current_question']][1][choix][1]  # Ajouter le score correspondant
        session['current_question'] += 1  # Passer à la question suivante
        
        if session['current_question'] >= len(questions):
            return redirect(url_for('resultat'))  # Aller aux résultats si fin du quiz
    
    question, reponses = questions[session['current_question']]
    return render_template('quiz.html', question=question, reponses=[r[0] for r in reponses])  # On n'affiche que les textes

@app.route('/resultat')
def resultat():
    score = session.get('score', 0)
    nom = session.get('nom', 'Inconnu')
    
    if score >= 50:
        verdict = "💖 C'est un homme à garder, il coche toutes les cases ! 💖"
    elif 35 <= score < 50:
        verdict = "🔍 Intéressant, mais à explorer davantage."
    elif 20 <= score < 35:
        verdict = "⚠️ Moyenne, il y a des signaux d’alerte."
    else:
        verdict = "🚨 Évite, il ne correspond pas à tes besoins."
    
    return render_template('resultat.html', nom=nom, score=score, verdict=verdict)

if __name__ == '__main__':
    app.run(debug=True)
