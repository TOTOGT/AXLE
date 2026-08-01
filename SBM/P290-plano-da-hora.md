# P290 — plano para a hora

**Quinta, 06/08/2026 · 16:00–17:00 · Saguão dos Anfiteatros do CCET**
Pôster: *Atratores Helicoidais em Variedades de Contato de Dimensão 3*

Levar: laptop com `maquinas.html` aberto, o pôster A0, e uma folha com a figura da
carapaça. Nada precisa de internet.

---

## O fio condutor

As três coisas — placa de Chladni, bacia do dm³, carapaça da tartaruga — são a mesma
pergunta:

> **Onde é que um sistema fica parado, e esse conjunto é simétrico?**

| | conjunto de repouso | simétrico? |
|---|---|---|
| Placa de Chladni | linhas nodais | **sim** (no quadrado) |
| dm³ | bacia de atração de Γ | **não** — r⋆ ≠ 2 − r⋆ |
| Carapaça | — | não (mais longa atrás) |

A assimetria **é** o resultado do pôster. Não precisa de coincidência numérica nenhuma
para justificar a sequência.

---

## Três profundidades (as pessoas chegam em níveis diferentes)

### 30 segundos — quem passa andando
Aponta para a placa no laptop, toca uma nota.

> "A areia foge de onde a placa vibra e se junta onde ela fica parada. Essas linhas
> são a solução de uma equação valendo zero. Meu pôster é sobre o mesmo tipo de
> conjunto, num sistema que não é uma placa."

Se pararem, sobe para 3 minutos.

### 3 minutos — a maioria
1. **A pergunta.** Um cilindro Γ = {r = 1} num espaço de contato. Ele atrai?
2. **Sim, e a taxa é exata:** μ = −2, o autovalor jacobiano. *(apontar fig. decay)*
3. **A surpresa:** a bacia não é simétrica. Por fora converge tudo até r = 3.
   Por dentro, colapsa abaixo de **r⋆ = 0,77594059**. *(apontar o painel azul)*
4. **Por que isso importa:** a assimetria é a impressão digital da direção
   não-integrável de α. Se fosse simétrica, o problema seria 2D disfarçado.

Fecha com: *"e esse número eu certifiquei — dá para você rodar em casa."*

### 10 minutos — quem tem interesse real
Acrescenta a **lei de escala**, que é o resultado novo:

- ε e z(0) não entram separados. Só entra λ = ε·e^(−z₀).
- Uma família de dois parâmetros vira **uma curva** r⋆(λ).
- Isso reconciliou duas coisas que pareciam contraditórias: r⋆ = 0,57224 em λ=1
  (a hipótese do teorema) e 0,77594 em λ=2 (a seção certificada).
- **A hipótese z(0) ≥ log 2 é necessária, não cosmética** — é ela que puxa r⋆ para
  baixo de 2/3 e faz a bola de Gronwall caber na bacia.

### 30 minutos — colega da área
Aqui entra a tartaruga, e entra **como problema aberto**, não como resultado.

---

## A tartaruga: liderar pela retratação

Esta é a conversa mais forte que você tem, e funciona porque começa admitindo o erro.

> "Eu tinha escrito que a proporção da carapaça codificava r⋆ ≈ 0,776 diretamente.
> Fui verificar e não se sustenta: r⋆ não é constante, é uma função r⋆(λ) que varre
> de 0,32 a 0,95. Isso cobre a razão de carapaça de qualquer espécie de tartaruga
> marinha. Uma grandeza que absorve qualquer medida não prevê nenhuma. Retratei no
> capítulo."

Depois, o que **sobra** e é verdade:

**Placa de Chladni e padrão de Turing resolvem o mesmo problema de autovalor.**
Mesmas autofunções cos(mπx/L)·cos(nπy/L), mesmos k admissíveis = π√(m²+n²)/L.
Mudam só em quem escolhe o modo:

- placa: k² vem da frequência de excitação
- Turing: k² vem da razão de difusão D_v/D_u

E o ponto que resiste à sua própria objeção (os parâmetros variam!):

> Perturbe a, b, D_u, D_v em ±25% e k_c varia 27%. Nenhum comprimento sobrevive.
> **Mas o modo selecionado é um inteiro.** Uma deriva de 25% em D_v não dá 4,7
> escudos — dá 5, ou dá 4. É por isso que a contagem de escudos é fixa por espécie
> (5 vertebrais, 4 pares costais) enquanto toda taxa subjacente varia com
> temperatura, ninhada e indivíduo.
>
> **O invariante é uma contagem, não uma razão.** Inteiros sobrevivem à deriva de
> parâmetros; 0,776 nunca poderia.

### A identificação certa: o sulco é a linha nodal

Se alguém perguntar *"onde fica o repouso na carapaça?"* — a resposta é: **onde os
escudos se encontram**. Simulação de reação-difusão (Brusselator, malha 90×90, bordas
de fluxo zero — a mesma condição de contorno de uma placa livre):

* **13 regiões desconexas** onde o campo se desloca → os escudos
* **1 região conexa** complementar → o conjunto zero, a rede de sulcos

Os escudos são ilhas; os sulcos são uma única rede conectada. É precisamente a
topologia da placa de Chladni: os ventres vibram em células isoladas, e a areia se
acumula numa rede conectada entre elas. **O sulco é a linha nodal.**

Contagem: 13 células contra ~10 pela estimativa linear — mesma ordem, a seleção
não-linear desloca um pouco. Honesto declarar assim.

> Isto é o que substitui a razão 0,776. Não é uma coincidência numérica: é a mesma
> topologia, pelo mesmo operador, na mesma condição de contorno.

**Marcadores de honestidade — dizer em voz alta:**
- O mecanismo de Turing para escudos de tartaruga é da literatura
  (Moustakas-Verho et al., *Development*, 2014). Não é meu.
- Que este modelo preveja **5 e 4** especificamente eu **não derivei**. Isso exigiria
  a geometria real da carapaça. `[MODELO]` com a contagem `[ABERTO]`.
- É exatamente aí que dados do TAMAR entrariam.

---

## Demonstração no laptop (`maquinas.html`)

Sequência de 90 segundos que funciona sem microfone:

1. **01 Placa Quadrada** + tom puro → mostra o conjunto nodal aparecendo
2. **03 Saturno** → "seis lados, e a simetria está verificada em Lean 4"
3. **05 Estrelamoto** → clicar: 18 → 30 → 93 → 150 Hz
   *"uma magnetar fraturou em 2004 e vibrou nessas frequências. Cada uma é um ℓ."*
4. **09 Batimento** → "é por isso que sinos de verdade tremem: não são redondos,
   e os modos degenerados se separam"

Se o saguão estiver silencioso, ligar o microfone e deixar a pessoa cantar. Só a
máquina 10 precisa dele.

---

## O que pedir

Não peça dinheiro no pôster. Peça duas coisas:

1. **Dados de carapaça do TAMAR** — quem tiver contato, isso fecha um problema aberto.
2. **Alguém que feche `kappa_lipschitz`** (AXLE #12). É um lema de Lipschitz. Um bom
   aluno de mestrado resolve.

Ambos são convites para colaborar, não pedidos. Funcionam muito melhor.

---

## Se perguntarem "você é de onde?"

Resposta curta e sem desculpas: *"Pesquisa independente, sem instituição. Tudo aberto,
CC BY 4.0 e MIT, e as provas que fechei estão verificadas em Lean 4 — onde eu não
consigo me enganar sozinho."*

Depois volta para a matemática.
