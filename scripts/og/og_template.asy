// ============================================================
// scripts/og/og_template.asy
//
// Open Graph image template
//
// Generated lecture-specific values:
//     __LECTURE_NUMBER__
//     __TITLE__
//     __CATEGORY__
//     __FILE__
//     __TAGS__
//     __GITHUB_USERNAME__
//     __REPO_NAME__
//     __ASY_TOP_SECTION__
//     __ASY_TARGET_EXAM__
//     __ASY_MOCKTITLE_A__
//     __ASY_MOCKTITLE_B__
//     __ASY_MOCKCARD_TOPIC__
//
// Output:
//     1200 × 630
// ============================================================

import graph;
import fontsize;



// Fix for complex LaTeX rendering & packages
usersetting();
texpreamble("\usepackage{amsmath}");


// ============================================================
// Canvas
// ============================================================

size(1200, 630);

real W = 1200;
real H = 630;


// ------------------------------------------------------------
// Color Palette (Premium Editorial Math Journal Slate Theme)
// ------------------------------------------------------------
pen bgCanvas    = rgb("#F7F9FC"); // Cream-tinged modern light gray
pen bgPanel     = rgb("#FFFFFF"); // Crisp white inner card
pen borderDark  = rgb("#0F172A"); // Slate-900 sharp border
pen primary     = rgb("#1E3A8A"); // Deep luxury ink blue
pen accentBlue  = rgb("#3B82F6"); // Vibrant engineering blue
pen textMain    = rgb("#334155"); // Slate-700 neutral dark
pen mathWater   = rgb("#CBD5E1"); // Slate-300 background math
pen gridLine    = rgb("#E2E8F0"); // Slate-200 geometry layout
pen gridFaint   = rgb("#F1F5F9"); // Super faint blueprint grid lines

// Left Promo Column Specific Pens
pen topBarBlue   = rgb("#0284C7");
pen badgeBgGreen = rgb("#E6F7F0"); 
pen badgeTxtGreen= rgb("#0D9488");
pen btnBgBlue    = rgb("#2563EB");

// ------------------------------------------------------------
// Standalone Native Rounded Box Helper
// ------------------------------------------------------------
path roundedBoxPath(pair A, pair B, real r) {
    real x1 = min(A.x, B.x), x2 = max(A.x, B.x);
    real y1 = min(A.y, B.y), y2 = max(A.y, B.y);
    return (x1+r, y1) -- (x2-r, y1) .. arc((x2-r, y1+r), r, -90, 0) -- 
           (x2, y2-r) .. arc((x2-r, y2-r), r, 0, 90) -- (x1+r, y2) .. 
           arc((x1+r, y2-r), r, 90, 180) -- (x1, y1+r) .. 
           arc((x1+r, y1+r), r, 180, 270) -- cycle;
}

// ------------------------------------------------------------
// Base Promo Layout Backdrop
// ------------------------------------------------------------
fill(box((0,0), (W,H)), bgCanvas);

// Top colored accent strip
fill(box((0, H-12), (W, H)), topBarBlue);

// Subtle underlying background mesh layer on the left area
for (real x = 40; x < 500; x += 40) {
    draw((x, 12)--(x, H - 12), gridFaint + linewidth(0.5));
}
for (real y = 40; y < H - 12; y += 40) {
    draw((12, y)--(500, y), gridFaint + linewidth(0.5));
}

// ============================================================
// LEFT SIDE BRAND CONTENT COLUMN
// ============================================================

// 1. Top Section Category Tag
path greenBadge = roundedBoxPath((60, 410), (460, 480), 12);
fill(greenBadge, badgeBgGreen);
label("__ASY_TOP_SECTION__", (260, 445), badgeTxtGreen + Helvetica("b") + fontsize(35));

// 2. High Impact Main Title Header
label("__CATEGORY__", (60, 345), E, borderDark + Helvetica("b") + fontsize(35));

// 3. Narrative Description Block
label("__TITLE__", (60, 265), E, textMain + Helvetica() + fontsize(22));
label("__ASY_NARRATIVE__", (60, 225), E, textMain + Helvetica() + fontsize(22));
// label("Lectures __LECTURE_NUMBER__", (60, 225), E, textMain + Helvetica() + fontsize(22));
label("__TAGS__", (60, 185), E, textMain + Helvetica() + fontsize(22));



// 4. Target Exam Access Buttons Group
path blueBadge = roundedBoxPath((60, 85), (420, 135), 8);
fill(blueBadge, btnBgBlue);
label("__ASY_TARGET_EXAM__", (240, 110), white + Helvetica("b") + fontsize(35));


// ============================================================
// RIGHT SIDE: PREMIUM MATH CARD GRAPHIC MOCKUP
// ============================================================
// Setting frame transformations coordinates mapping 1200x630 space to relative card box
// Card box dimensions: Width=620, Height=325.5 (Preserves precise 1200:630 aspect ratio)
pair mockOrigin = (530, 135); 
real s = 0.52; // Absolute uniform geometry scale modifier parameter

// Helper utility closure to transform relative coordinates cleanly onto mock preview space
pair tf(real origX, real origY) {
    return mockOrigin + (origX * s, origY * s);
}

// Base drop-shadow backdrop plate behind card mockup frame
path cardShadow = roundedBoxPath(tf(16,16) - (0,3), tf(1200-16, 630-16) - (0,3), 24 * s);
fill(cardShadow, rgb("#E2E8F0"));

// Main Outer Card Mockup Shell Frame
path mockCanvasFrame = roundedBoxPath(tf(16, 16), tf(1200-16, 630-16), 24 * s);
fill(mockCanvasFrame, bgPanel);
draw(mockCanvasFrame, borderDark + linewidth(2.5 * s));

// Subtle internal blueprint gridding lines inside card layout matrix
for (real x = 40; x < 1200 - 20; x += 40) {
    draw(tf(x, 20)--tf(x, 630 - 20), gridFaint + linewidth(0.5 * s));
}
for (real y = 40; y < 630 - 20; y += 40) {
    draw(tf(20, y)--tf(1200 - 20, y), gridFaint + linewidth(0.5 * s));
}

// ------------------------------------------------------------
// MOCK CARD CONTENT: REFINED WATERMARKS
// ------------------------------------------------------------
label("$\begin{pmatrix} \cos\theta \\& -\sin\theta \\ \sin\theta \\& \cos\theta \end{pmatrix}$", tf(170, 535), mathWater + fontsize(14 * s));
label("$\oint_C \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S}$", tf(1010, 545), mathWater + fontsize(13 * s));
label("$e^{i\pi} + 1 = 0$", tf(1010, 505), mathWater + fontsize(16 * s));

// ------------------------------------------------------------
// MOCK CARD CONTENT: LEFT GEOMETRY WIDGET
// ------------------------------------------------------------
pair mockC = tf(150, 340);
real mockGeomR = 60 * s;

draw(circle(mockC, mockGeomR), gridLine + linewidth(1 * s));
draw((mockC.x - mockGeomR - 15*s, mockC.y)--(mockC.x + mockGeomR + 15*s, mockC.y), gridLine + linewidth(0.6 * s));
draw((mockC.x, mockC.y - mockGeomR - 15*s)--(mockC.x, mockC.y + mockGeomR + 15*s), gridLine + linewidth(0.6 * s));

pair mockP = mockC + mockGeomR*dir(38);
draw(mockC--mockP, accentBlue + linewidth(1.5 * s));
dot(mockC, primary + linewidth(4 * s));
label("$r$", mockC + (22*s, 24*s), mathWater + fontsize(12 * s));
label("$\theta$", mockC + (16*s, 6*s), mathWater + fontsize(11 * s));

// ------------------------------------------------------------
// MOCK CARD CONTENT: RIGHT FUNCTION GRAPH
// ------------------------------------------------------------
real mgx1 = 930, mgx2 = 1110;
real mgy  = 340;

draw(tf(mgx1, mgy)--tf(mgx2, mgy), gridLine + linewidth(0.8 * s));
draw(tf(1020, 270)--tf(1020, 410), gridLine + linewidth(0.8 * s));

real mockPoly(real x) {
  real t = (x - 1020)/50;
  return mgy - 25*t + 12*t^3; 
}
draw(graph(new real(real x) { return tf(x, mockPoly(x)).y; }, mgx1, mgx2, n=100), accentBlue + linewidth(1.2 * s));

// ------------------------------------------------------------
// MOCK CARD CONTENT: CENTER TYPOGRAPHY & EMBLEM
// ------------------------------------------------------------
pair mockEmblem = tf(600, 485);
fill(circle(mockEmblem, 36 * s), primary);
label("$\sum$", mockEmblem, white + fontsize(36 * s));

draw(tf(420, 485)--tf(535, 485), accentBlue + linewidth(1 * s));
draw(tf(665, 485)--tf(780, 485), accentBlue + linewidth(1 * s));
dot(tf(535, 485), accentBlue + linewidth(3 * s));
dot(tf(665, 485), accentBlue + linewidth(3 * s));

pen mockTitleFont = Palatino(series="b", shape="n") + fontsize(56 * s);
label("__ASY_MOCKTITLE_A__", tf(600, 395), primary + mockTitleFont);
label("__ASY_MOCKTITLE_B__", tf(600, 325), primary + mockTitleFont);

draw(tf(480, 292)--tf(720, 292), gridLine + linewidth(1.2 * s));
// label("Rigorous Notes  $\cdot$  Curated Problem Sets  $\cdot$  Visual Proofs", tf(600, 262), textMain + fontsize(16 * s));


// ------------------------------------------------------------
// MOCK CARD CONTENT: TOPIC BADGE PILL
// ------------------------------------------------------------
path mockBadgeBox = roundedBoxPath(tf(120, 192), tf(1080, 230), 6 * s);
fill(mockBadgeBox, rgb("#EFF6FF")); 
draw(mockBadgeBox, accentBlue + linewidth(1 * s));

pen mockBadgeFont = Palatino(series="b", shape="n") + fontsize(30 * s);
label("__ASY_MOCKCARD_TOPIC__", tf(600, 211), primary + mockBadgeFont);


// ============================================================
// MOCK CARD CONTENT: FOOTER TRACK & URL (BRIGHT THEME OPTIMIZED)
// ============================================================
real mBaseY = 60;
real mWaveA(real x) { return mBaseY + 12 * sin(0.025 * x); }
real mWaveB(real x) { return mBaseY + 8 * cos(0.035 * x + 0.5); }

draw(graph(new real(real x) { return tf(x, mWaveA(x)).y; }, 30, 1200 - 30, n=150), gridLine + linewidth(1 * s));
draw(graph(new real(real x) { return tf(x, mWaveB(x)).y; }, 30, 1200 - 30, n=150), mathWater + linewidth(0.8 * s));

for (int i = 1; i <= 10; ++i) {
    real dotX = 40 + i * 105;
    if (dotX < 430 || dotX > 770) {
        dot(tf(dotX, mWaveA(dotX)), primary + linewidth(4 * s));
        dot(tf(dotX + 25, mWaveB(dotX + 25)), accentBlue + linewidth(3 * s));
    }
}

// Construct transformed pairs directly to avoid winding rule blackouts
pair fMinTrans = tf(230, 70);
pair fMaxTrans = tf(970, 130);
real finalRadius = 10 * s;

// Soft, transparent drop shadow behind the pill container
path mockShadowBox = roundedBoxPath(fMinTrans + (0, -2 * s), fMaxTrans + (0, -2 * s), finalRadius);
//fill(mockShadowBox, rgb("#E2E8F0"));
// Soft, transparent drop shadow behind the pill container
//fill(mockShadowBox, rgb("#EAE7DC")); // Warm sandstone shadow tint

// Front Pill Layer: Soft, vibrant ice blue backdrop instead of borderDark
path mockFooterBox = roundedBoxPath(fMinTrans, fMaxTrans, finalRadius);
//fill(mockFooterBox, rgb("#EFF6FF")); // Premium light blue container
// Front Pill Layer: Luxury academic ivory page texture
fill(mockFooterBox, rgb("#FAF8F5")); // Crisp warm alabaster ivory
draw(mockFooterBox, primary + linewidth(1 * s)); // Sharp thin accent boundary line


// Contrast Label text layered cleanly on top (swapped from white to deep primary ink)
pen mockUrlFont = Palatino(series="b", shape="n") + fontsize(45 * s);
label("https://__GITHUB_USERNAME__.github.io/__REPO_NAME__/", tf(600, 100), primary + mockUrlFont);
