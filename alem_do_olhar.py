#!/usr/bin/env python3
# -- coding: utf-8 --
"""
Além do Olhar — Réplica Completa do Site em Python
--------------------------------------------------
Execute no terminal:
    python alem_do_olhar.py

O script iniciará um servidor HTTP local e abrirá automaticamente
a réplica interativa no seu navegador padrão.
"""

import http.server
import socketserver
import threading
import webbrowser
import json

PORT = 8000

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Além do Olhar</title>
  <style>
    :root {
      --bg: #070d1e;
      --card-bg: #0f172a;
      --card-border: #1e293b;
      --accent: #f97316;
      --accent-hover: #ea580c;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --danger: #ef4444;
      --success: #10b981;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding-bottom: 80px;
    }
    header {
      width: 100%;
      max-width: 600px;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--card-border);
    }
    .logo {
      font-size: 1.25rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .logo span { color: var(--accent); }
    main {
      width: 100%;
      max-width: 600px;
      padding: 20px;
      flex: 1;
    }
    .hero {
      text-align: center;
      padding: 30px 10px;
      background: linear-gradient(180deg, rgba(249, 115, 22, 0.08) 0%, transparent 100%);
      border-radius: 20px;
      margin-bottom: 24px;
    }
    .hero h1 {
      font-size: 1.8rem;
      margin-bottom: 12px;
      line-height: 1.2;
    }
    .hero p {
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.5;
      margin-bottom: 20px;
    }
    .btn {
      background: var(--accent);
      color: #fff;
      border: none;
      padding: 12px 24px;
      border-radius: 9999px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
    }
    .btn:hover { background: var(--accent-hover); }
    .btn:active { transform: scale(0.98); }
    .btn-outline {
      background: transparent;
      border: 1px solid var(--card-border);
      color: var(--text);
    }
    .btn-outline:hover { background: var(--card-border); }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 16px;
    }
    .card-title {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 8px;
    }
    .tag {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      background: rgba(249, 115, 22, 0.15);
      color: var(--accent);
      margin-bottom: 12px;
    }
    .grid { display: grid; gap: 12px; }

    /* Quiz */
    .quiz-options {
      display: flex;
      gap: 12px;
      margin-top: 16px;
    }
    .btn-mito {
      flex: 1;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #fca5a5;
      padding: 12px;
      border-radius: 12px;
      font-weight: 600;
      cursor: pointer;
    }
    .btn-realidade {
      flex: 1;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #6ee7b7;
      padding: 12px;
      border-radius: 12px;
      font-weight: 600;
      cursor: pointer;
    }
    .feedback {
      margin-top: 16px;
      padding: 16px;
      border-radius: 12px;
      font-size: 0.9rem;
      line-height: 1.4;
      display: none;
    }
    .feedback.correct {
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid var(--success);
      color: #a7f3d0;
    }
    .feedback.wrong {
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid var(--danger);
      color: #fecaca;
    }

    /* Acolhimento - Respiração */
    .breath-box {
      text-align: center;
      padding: 30px 0;
    }
    .circle {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      background: rgba(249, 115, 22, 0.2);
      border: 3px solid var(--accent);
      margin: 0 auto 20px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
      font-weight: bold;
      color: #fff;
      transition: transform 4s ease-in-out;
    }
    .circle.inhale { transform: scale(1.4); }
    .circle.hold { transform: scale(1.4); }
    .circle.exhale { transform: scale(1); }

    /* Barra Inferior */
    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      background: #091124;
      border-top: 1px solid var(--card-border);
      display: flex;
      justify-content: space-around;
      padding: 10px 0;
      z-index: 50;
    }
    .nav-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      font-size: 0.75rem;
      color: var(--text-muted);
      cursor: pointer;
      text-decoration: none;
      background: none;
      border: none;
    }
    .nav-item.active { color: var(--accent); font-weight: 600; }

    /* Caixas de ajuda / não ajuda */
    .box-do {
      background: rgba(16, 185, 129, 0.1);
      border-left: 4px solid var(--success);
      padding: 12px;
      border-radius: 0 8px 8px 0;
      font-size: 0.85rem;
      margin-top: 8px;
    }
    .box-dont {
      background: rgba(239, 68, 68, 0.1);
      border-left: 4px solid var(--danger);
      padding: 12px;
      border-radius: 0 8px 8px 0;
      font-size: 0.85rem;
      margin-top: 8px;
    }
  </style>
</head>
<body>

  <header>
    <div class="logo">👁️ Além do <span>Olhar</span></div>
    <span style="font-size: 0.8rem; color: var(--text-muted);">Réplica Local</span>
  </header>

  <main id="app">
    <!-- Telas gerenciadas dinamicamente via JS -->
  </main>

  <nav class="bottom-nav">
    <button class="nav-item active" onclick="navigate('home')">🏠 Início</button>
    <button class="nav-item" onclick="navigate('exp')">🎭 Vivências</button>
    <button class="nav-item" onclick="navigate('quiz')">❓ Quiz</button>
    <button class="nav-item" onclick="navigate('acolha')">💚 Acolha</button>
    <button class="nav-item" onclick="navigate('apoio')">📞 Apoio</button>
  </nav>

  <script>
    const EXPERIENCES = [
      {
        id: 1,
        title: "5 minutos antes da apresentação",
        tag: "Saúde Mental",
        desc: "O coração acelera, as mãos suam e o pensamento antecipa o fracasso diante do público.",
        dont: "Não diga: 'É só nervosismo bobo, relaxa e vai!'.",
        do: "Valide o sentimento: 'Estou aqui com você. Respire no seu tempo.'",
        challenge: "Você sente a respiração curta. Qual é o melhor próximo passo?",
        options: [
          { text: "Tentar forçar a fala imediatamente", feedback: "Pode aumentar a sensação de bloqueio." },
          { text: "Fazer pausas de respiração 4-4-4", feedback: "Excelente! Reduz o disparo de cortisol e acalma o sistema nervoso." }
        ]
      },
      {
        id: 2,
        title: "O refeitório na hora do almoço",
        tag: "Neurodiversidade (TEA)",
        desc: "O tilintar dos talheres, conversas sobrepostas e luzes fortes tornam o espaço insuportável.",
        dont: "Não force a permanência ou insista que 'todo mundo se acostuma'.",
        do: "Ofereça um local silencioso ou incentive o uso de abafadores de ruído.",
        challenge: "O barulho está no ápice. O que fazer?",
        options: [
          { text: "Ignorar e forçar a conversa", feedback: "Aumenta o risco de crise por sobrecarga sensorial." },
          { text: "Recuar para um ambiente neutro e usar abafadores", feedback: "Correto! Respeita os limites sensoriais da pessoa." }
        ]
      },
      {
        id: 3,
        title: "Atravessando a rua",
        tag: "Baixa Visão",
        desc: "Faróis ofuscam, buracos somem no asfalto e a travessia exige máxima atenção auditiva.",
        dont: "Nunca puxe a pessoa pelo braço ou pela bengala sem avisar.",
        do: "Pergunte antes: 'Você gostaria de ajuda para atravessar?' e ofereça o seu cotovelo.",
        challenge: "Você encontra alguém com bengala na esquina. Qual a atitude correta?",
        options: [
          { text: "Puxar a pessoa rápido pelo braço", feedback: "Perigoso! Desorienta o equilíbrio e invade o espaço da pessoa." },
          { text: "Perguntar com calma se ela deseja apoio", feedback: "Perfeito! Mantém a autonomia e a segurança." }
        ]
      }
    ];

    const QUIZ = [
      {
        q: "Toda pessoa autista não gosta de contato visual?",
        ans: "MITO",
        exp: "O autismo é um espectro. Cada indivíduo possui preferências e características sensoriais únicas."
      },
      {
        q: "Uma pessoa com depressão pode sorrir e ter momentos descontraídos?",
        ans: "REALIDADE",
        exp: "Depressão é um quadro clínico complexo. A pessoa não fica necessariamente triste o tempo todo."
      },
      {
        q: "Ansiedade é apenas falta de confiança pessoal?",
        ans: "MITO",
        exp: "A ansiedade envolve reações psicofisiológicas reais e pode acontecer mesmo com pessoas seguras."
      },
      {
        q: "Ao ajudar uma pessoa cega, deve-se perguntar antes de agir?",
        ans: "REALIDADE",
        exp: "Sempre pergunte antes. Pessoas com deficiência visual possuem autonomia e técnicas próprias de locomoção."
      }
    ];

    let currentScreen = 'home';
    let quizIndex = 0;
    let quizScore = 0;

    function renderHome() {
      return `
        <div class="hero">
          <h1>Você conhece a realidade que não consegue enxergar?</h1>
          <p>Uma plataforma interativa para experimentar e compreender a neurodiversidade, a saúde mental e a acessibilidade.</p>
          <button class="btn" onclick="navigate('exp')">Viver uma experiência</button>
        </div>
        <div class="card">
          <div class="tag">Sobre a proposta</div>
          <div class="card-title">Empatia em primeira pessoa</div>
          <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">
            Coloque-se no lugar de quem enfrenta sobrecargas sensoriais, crises de ansiedade ou barreiras de acessibilidade no cotidiano.
          </p>
        </div>
      `;
    }

    function renderExp() {
      return `
        <h2 style="margin-bottom: 16px;">Vivências Interativas</h2>
        ${EXPERIENCES.map((e, idx) => `
          <div class="card">
            <span class="tag">${e.tag}</span>
            <div class="card-title">${e.title}</div>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 12px;">${e.desc}</p>
            <div class="box-dont"><strong>O que NÃO ajuda:</strong> ${e.dont}</div>
            <div class="box-do"><strong>O que pode ajudar:</strong> ${e.do}</div>
            <div style="margin-top: 14px;">
              <p style="font-weight: 600; font-size: 0.85rem; margin-bottom: 8px;">${e.challenge}</p>
              ${e.options.map(opt => `
                <button class="btn btn-outline" style="width: 100%; text-align: left; margin-bottom: 6px; font-size: 0.85rem;" onclick="alert('${opt.feedback}')">
                  • ${opt.text}
                </button>
              `).join('')}
            </div>
          </div>
        `).join('')}
      `;
    }

    function renderQuiz() {
      if (quizIndex >= QUIZ.length) {
        return `
          <div class="card" style="text-align: center; padding: 30px;">
            <h2>Quiz Concluído!</h2>
            <p style="margin: 16px 0; font-size: 1.1rem; color: var(--accent);">Você acertou ${quizScore} de ${QUIZ.length} afirmações.</p>
            <button class="btn" onclick="quizIndex=0; quizScore=0; navigate('quiz')">Recomeçar Quiz</button>
          </div>
        `;
      }
      const item = QUIZ[quizIndex];
      return `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <h2>Mito ou Realidade?</h2>
          <span style="color: var(--text-muted); font-size: 0.85rem;">${quizIndex + 1} de ${QUIZ.length}</span>
        </div>
        <div class="card">
          <p style="font-size: 1.1rem; font-weight: 600; line-height: 1.4;">${item.q}</p>
          <div class="quiz-options">
            <button class="btn-mito" onclick="answerQuiz('MITO')">MITO</button>
            <button class="btn-realidade" onclick="answerQuiz('REALIDADE')">REALIDADE</button>
          </div>
          <div id="quiz-feedback" class="feedback"></div>
        </div>
      `;
    }

    function answerQuiz(userAns) {
      const item = QUIZ[quizIndex];
      const fb = document.getElementById('quiz-feedback');
      const isCorrect = userAns === item.ans;
      if (isCorrect) quizScore++;

      fb.className = 'feedback ' + (isCorrect ? 'correct' : 'wrong');
      fb.innerHTML = <strong>${isCorrect ? 'Correto!' : 'Incorreto!'}</strong> É um(a) ${item.ans}.<br><br>${item.exp}<br><br><button class="btn" style="padding: 6px 14px; font-size: 0.8rem;" onclick="quizIndex++; navigate('quiz');">Próxima pergunta</button>;
      fb.style.display = 'block';
    }

    function renderAcolha() {
      return `
        <h2 style="margin-bottom: 16px;">Na Crise, Acolha</h2>
        <div class="card breath-box">
          <div class="card-title">Respiração Guiada 4-4-4</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 20px;">Inspire, segure e solte o ar suavemente para desacelerar o ritmo cardíaco.</p>
          <div id="circle" class="circle">Inspire</div>
          <button class="btn" onclick="toggleBreathing()">Iniciar Ciclo</button>
        </div>
        <div class="card">
          <div class="card-title">SOS Rápido</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.5;">
            Se você estiver se sentindo sobrecarregado:
            <br>• Beba um copo d'água devagar;
            <br>• Coloque os pés firmes no chão (técnica de ancoragem);
            <br>• Reduza luzes e fontes de barulho ao redor.
          </p>
        </div>
      `;
    }

    let breathInterval = null;
    function toggleBreathing() {
      const c = document.getElementById('circle');
      if (breathInterval) {
        clearInterval(breathInterval);
        breathInterval = null;
        c.innerText = 'Inspire';
        c.className = 'circle';
        return;
      }
      let step = 0;
      const steps = [
        { text: 'Inspire (4s)', cls: 'inhale' },
        { text: 'Segure (4s)', cls: 'hold' },
        { text: 'Expire (4s)', cls: 'exhale' }
      ];
      const run = () => {
        c.innerText = steps[step].text;
        c.className = 'circle ' + steps[step].cls;
        step = (step + 1) % steps.length;
      };
      run();
      breathInterval = setInterval(run, 4000);
    }

    function renderApoio() {
      return `
        <h2 style="margin-bottom: 16px;">Canais de Apoio e Emergência</h2>
        <div class="card">
          <div class="card-title">CVV — Centro de Valorização da Vida</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px;">Apoio emocional gratuito e 24h por telefone.</p>
          <a href="tel:188" class="btn" style="text-decoration: none; display: inline-block;">Ligar 188</a>
        </div>
        <div class="card">
          <div class="card-title">SAMU — Atendimento Móvel de Urgência</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px;">Em emergências médicas ou psiquiátricas graves.</p>
          <a href="tel:192" class="btn btn-outline" style="text-decoration: none; display: inline-block;">Ligar 192</a>
        </div>
        <div class="card">
          <div class="card-title">CAPS — Centros de Atenção Psicossocial</div>
          <p style="color: var(--text-muted); font-size: 0.85rem;">Procure a unidade do CAPS mais próxima no seu município para suporte psicológico contínuo pelo SUS.</p>
        </div>
      `;
    }

    function navigate(screen) {
      currentScreen = screen;
      document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
      const app = document.getElementById('app');
      if (screen === 'home') app.innerHTML = renderHome();
      else if (screen === 'exp') app.innerHTML = renderExp();
      else if (screen === 'quiz') app.innerHTML = renderQuiz();
      else if (screen === 'acolha') app.innerHTML = renderAcolha();
      else if (screen === 'apoio') app.innerHTML = renderApoio();
      window.scrollTo(0, 0);
    }

    // Inicialização
    navigate('home');
  </script>
</body>
</html>
"""

class SiteHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))

    def log_message(self, format, *args):
        # Silencia logs para deixar o terminal limpo
        pass

def main():
    with socketserver.TCPServer(("", PORT), SiteHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print(" ALÉM DO OLHAR — Servidor Local Ativo")
        print(f" Acesse em seu navegador: {url}")
        print(" Pressione Ctrl+C para encerrar o servidor.")
        print("=" * 60)

        # Abre o navegador automaticamente
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado com sucesso.")

if _name_ == "_main_":
    main()
S
