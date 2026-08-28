#import "../../templates/course.typ": *

== Fields

#example[
  The following are examples of fields.
  - The field of rational numbers $QQ$.
  - The field of real numbers $RR$.
  - The field of complex numbers $CC$.
  - For any prime number $p$, 
    the ring $ZZ slash p ZZ$ of integers modulo $p$ is a field, denoted by $FF_p$.
  - For any prime number $p$ and positive integer $n$, there exists a unique (up to isomorphism) finite field of order $p^n$, denoted by $FF_(p^n)$.
]

#exer[
  Show that the following are not fields.
  - The ring of integers $ZZ$.
  - The ring of polynomials $QQ[x]$ in one variable $x$ over $QQ$.
  - The ring of polynomials $RR[x, y]$ in two variables $x, y$ over $RR$.
]

#exer[
  Show that any finite integral domain is a field.
]

#exer[
  Show that any finite field has order $p^n$ for some prime number $p$ and positive integer $n$.
]

#example("Field of Rational Functions")[
  For any field $k$, the ring of polynomials in one variable $x$ over $k$ is 
  denoted by $k[x]$.
  The field of rational functions in one variable $x$ over $k$ is denoted by $k(x)$,
  and it consists of all elements of the form $f(x) / g(x)$, where $f(x), g(x) in k[x]$ and $g(x) eq.not 0$.
  The field $k(x)$ is the field of fractions of the integral domain $k[x]$,  
  and it is called the *field of rational functions* in one variable $x$ over $k$.
  // The field $k(x)$ can also be viewed as the *function field* of the affine line over $k$.
]

#example("Field of Laurent Series")[
  For any field $k$, the *ring of formal power series* in one variable $x$ over $k$ is 
  denoted by $k[[x]]$.
  The *field of formal Laurent series* in one variable $x$ over $k$ is denoted by $k((x))$,
  and it consists of the generalized formal power series,
  that is, all elements of the form 
  $
    sum_(n gt.eq n_0) a_n x^n
  $
  for some integer $n_0$, where $a_n in k$ for all $n gt.eq n_0$ and $a_(n_0) eq.not 0$.
  The field $k((x))$ is the field of fractions of the integral domain $k[[x]]$,  
  and it is called the *field of formal Laurent series* in one variable $x$ over $k$.
]

== Field homomorphisms and isomorphisms

#defn[
  Let $K$ and $L$ be fields. A *field homomorphism* from $K$ to $L$ is a map $sigma colon K arrow L$ that preserves the field operations, that is, for all $a, b in K$, we have
  - $sigma(a + b) = sigma(a) + sigma(b)$,
  - $sigma(a b) = sigma(a) sigma(b)$,
  - $sigma(1_K) = 1_L$, where $1_K$ and $1_L$ denote the multiplicative identities of $K$ and $L$, respectively.
  A homomorphism $sigma colon K arrow L$ is called an 
  *isomorphism* if there exists a homomorphism $tau colon L arrow K$ such that $tau compose sigma = id_K$ and $sigma compose tau = id_L$, where $id_K$ and $id_L$ denote the identity maps on $K$ and $L$, respectively.
]

#exer[
  Show that if $sigma colon K arrow L$ is a field homomorphism, then $sigma$ is injective. Is it true that $sigma$ is surjective? If yes, prove it. If not, give a counterexample.
]

#exer[
  Let $sigma colon K arrow L$ be a field homomorphism. Show that $sigma$ is an isomorphism if and only if $sigma$ is surjective.
]

== Extension of fields

#defn[
  Let $K$ be a field. A *field extension* of $K$ is a field $L$ that contains $K$ as a subfield. We often denote a field extension by $L slash K$, which indicates that $L$ is an extension of $K$. The field $K$ is called the *base field*, and the field $L$ is called the *extension field*.
]

#example[
  - The field of complex numbers $CC$ is an extension of the field of real numbers $RR$. 
  - Similarly, the field of real numbers $RR$ is an extension of the field of rational numbers $QQ$.
  - For any field $k$, the field of rational functions $k(x)$ in one variable $x$ over $k$ is an extension of $k$.
  - For any field $k$, the field of formal Laurent series $k((x))$ in one variable $x$ over $k$ is an extension of $k$.
]

#defn[
  Let $L slash K$ be a field extension. An *intermediate extension* of $L slash K$ is a field $M$ such that $K subset.eq M subset.eq L$. In this case, we say that $M slash K$ is a subextension of $L slash K$.
]

#example[
  For any field $k$, the field of rational functions $k(x)$ in one variable $x$ over $k$ is an extension of $k$. The field of rational functions $k(x^2)$ in one variable $x^2$ over $k$ is an intermediate extension of $k(x) slash k$.
]

#example[
  For any field $k$, the field of formal Laurent series $k((x))$ in one variable $x$ over $k$ is an extension of $k$. 
  The field of formal rational functions $k(x)$ in one variable $x$ over $k$ is an intermediate extension of $k((x)) slash k$.
]

#exer[
  Let $k$ be a field, and let $k(t)$ be the field of rational functions in one variable $t$ over $k$. 
  Show that any element of $k(t)$ is a root of some quadratic polynomial with coefficients in $k(t^2)$.
  Determine all field homomorphisms from $k(t)$ to itself that fix $k(t^2)$ pointwise.
]

== Generated subfields

#defn[
  Let $L slash K$ be a field extension. 
  Let $S$ be a subset of $L$. 
  The *field generated by $S$ over $K$*, denoted by $K(S)$, is defined to be the smallest subfield of $L$ that contains both $K$ and $S$.
  We say that the field extension $L slash K$ is *generated by $S$* if $L = K(S)$.
  The *ring generated by $S$ over $K$*, denoted by $K[S]$, is defined to be the smallest subring of $L$ that contains both $K$ and $S$.
]

#remark[
  Note that the field generated by $S$ over $K$ 
  is the intersection of all subfields of $L$ that contain both $K$ and $S$.
  Similarly, the ring generated by $S$ over $K$
  is the intersection of all subrings of $L$ that contain both $K$ and $S$.
]

#defn[
  Let $L slash K$ be a field extension. We say that the extension $L slash K$ is *finitely generated* if there exists a finite subset $S subset L$ such that $L = K(S)$.
]

#exer[
  Let $k$ be a field. Consider the field extension 
  $k(x_1, x_2, dots, x_n) slash k$, where $k(x_1, x_2, dots, x_n)$ is 
  the field of rational functions in $n$ variables $x_1, x_2, dots, x_n$ over $k$. 
  Show that $k(x_1, x_2, dots, x_n)$ is generated by 
  the elements $x_1, x_2, dots, x_n$ over $k$, that is, 
  show that $k(x_1, x_2, dots, x_n) = k({x_1, x_2, dots, x_n})$.
  Also show that the ring $k[x_1, dots, x_n]$ of polynomials 
  in $n$ variables $x_1, dots, x_n$ over $k$ 
  is generated by the elements $x_1, dots, x_n$ over $k$, 
  that is, show that $k[x_1, dots, x_n] = k[{x_1, dots, x_n}]$.
]

#remark[
  The field of rational functions $k(x_1, x_2, dots, x_n)$ in $n$ variables $x_1, x_2, dots, x_n$ over $k$ is the field of fractions of the integral domain $k[x_1, dots, x_n]$ of polynomials in $n$ variables $x_1, dots, x_n$ over $k$.
  Moreover, 
  the field $k(x_1, x_2, dots, x_n)$ is generated by 
  the elements $x_1, x_2, dots, x_n$ over $k$, and hence,  
  the extension $k(x_1, x_2, dots, x_n) slash k$ is finitely generated.
  Furthermore, the ring $k[x_1, dots, x_n]$ is generated by the elements $x_1, dots, x_n$ over $k$.
]

#exer[
  Let $L slash K$ be a field extension, and let $S$ be a subset of $L$. 
  Show that the field generated by $S$ over $K$ is equal to the set of all elements of $L$ that can be expressed as a rational function in the elements of $S$ with coefficients in $K$. In other words, show that
  $
    K(S) = 
    union.big_(S_f subset S, \ |S_f| < infinity) K(S_f)
    .
  $
  Also show that the ring generated by $S$ over $K$ is equal to the set of all elements of $L$ that can be expressed as a polynomial in the elements of $S$ with coefficients in $K$. In other words, show that
  $
    K[S] = 
    union.big_(S_f subset S, \ |S_f| < infinity) K[S_f]
    .
  $
]

#remark[
  Let $L slash K$ be a field extension, 
  and let $alpha_1, alpha_2, dots, alpha_n in L$.
  Then the field $K({alpha_1, alpha_2, dots, alpha_n})$ is also denoted by $K(alpha_1, alpha_2, dots, alpha_n)$.
]

#exer[
  Show that the fields $QQ(sqrt(2)), QQ(sqrt(3))$
  are not isomorphic.
  What can be said about the fields $QQ(sqrt(2), sqrt(6)), QQ(sqrt(3), sqrt(6))$?
]

#exer[
  Show that $QQ(sqrt(2))$ is equal to $QQ[{sqrt(2)}]$.
]

#exer[
  Show that $QQ(sqrt(2), sqrt(3))$ is equal to $QQ(sqrt(2) + sqrt(3))$.
]

#exer[
  Show that $QQ(sqrt(2), omega)$ is equal to $QQ(sqrt(2) + omega)$, where $omega$ denotes a primitive cube root of unity in $CC$.
]

#example[
  Let $n$ be a positive integer, and let $zeta_n$ denote a primitive $n$-th root of unity in $CC$. 
  Then the extension $QQ(zeta_n)$ of $QQ$, generated $zeta_n$, 
  is called the *cyclotomic extension* of $QQ$ 
  obtained by adjoining the $n$-th roots of unity.
]

#exer[
  Determine the degree of the cyclotomic extension $QQ(zeta_n)$ over $QQ$ for $n = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10$.
]

== Degree of field extensions

If $L slash K$ is a field extension, then $L$ can be viewed as a vector space over $K$, where scalar multiplication is given by the field multiplication. In particular, we can consider the dimension of $L$ as a vector space over $K$.

#exer[
  Show that the map
  $
    CC times CC arrow CC, (a, b) mapsto overline(a) b,
  $
  where $overline(a)$ denotes the complex conjugate of $a$,
  defines a $CC$-linear structure on $CC$ that makes $CC$ into a vector space over $CC$.
]

#defn[
  Let $L slash K$ be a field extension. We say that $L$ is a *finite extension* of $K$ if $L$ is a finite-dimensional vector space over $K$. In this case, we define the *degree* of the extension $L slash K$ to be the dimension of $L$ as a vector space over $K$, and we denote it by $[L : K]$. If $L$ is not finite-dimensional over $K$, we say that the extension is *infinite*.
]

#exer[
  Let $L slash K$ be a field extension.
  Show that the degree of the extension $L slash K$ is equal to $1$ if and only if $L = K$.
]

#exer[
  Show that $[k(x) : k] = infinity$ for any field $k$.
]

#exer[
  Show that $k(t) slash k(t^2)$ is a finite extension of degree $2$.
]

#exer[
  Determine the degrees of the following extensions.
  $
    QQ(sqrt(2)) slash QQ,
    QQ(sqrt(2), sqrt(3)) slash QQ,
    QQ(sqrt(2), root(3, 3)) slash QQ,
    QQ(sqrt(2), sqrt(3), sqrt(5)) slash QQ.
  $
]

#exer[
  Determine the degrees of the following extensions over $QQ$.
  $
    QQ(i), QQ(omega), QQ(zeta_n).
  $
]

#exer[
  Let $L slash K$ be a field extension. Show that if $L slash K$ is a finite extension of degree $n$, then any element of $L$ is a root 
  of a polynomial of degree at most $n$ with coefficients in $K$.
]

Now let's look at some examples of finite extensions.

#example[
  Consider the field extension $QQ(sqrt(2)) slash QQ$. We claim that this is a finite extension of degree $2$. To see this, note that any element of $QQ(sqrt(2))$ can be written in the form $a + b sqrt(2)$ for some $a, b in QQ$. The set $B = {1, sqrt(2)}$ is linearly independent over $QQ$, and it spans $QQ(sqrt(2))$, so it forms a basis. Therefore, the dimension of $QQ(sqrt(2))$ as a vector space over $QQ$ is $2$, and we have $[QQ(sqrt(2)) : QQ] = 2$.
]

#lemma[
  Let $L slash K$, $K slash F$ be field extensions. 
  If $L slash K, K slash F$ are finite extensions, then 
  so is $L slash F$, and the degrees of these extensions satisfy
  $ 
  [L : F] = [L : K] [K : F].
  $
]

#proof[
  Note that if the degree of the extension $K slash F$ is infinite, then
  observing that $K$ is an $F$-subspace of $L$,
  it follows that the degree of the extension $L slash F$ is also infinite.
  Also note that if the degree of the extension $L slash K$ is infinite, then
  the degree of the extension $L slash F$ is also infinite, since 
  any subset of $L$ that generates $L$ as a $K$-vector space also generates $L$ as an $F$-vector space.
  This shows that if either $[L : K]$ or $[K : F]$ is infinite, then $[L : F]$ is also infinite.

  Let ${u_1, u_2, dots, u_m}$ be a basis of $L$ over $K$, 
  and let ${v_1, v_2, dots, v_n}$ be a basis of $K$ over $F$. 
  We claim that the set
  $
    B = {u_i v_j : 1 lt.eq i lt.eq m, 1 lt.eq j lt.eq n}
  $ 
  is a basis of $L$ over $F$.
  Indeed, for any $alpha in L$, we can write 
  $
    alpha = sum_(i=1)^m c_i u_i
  $
  for some $c_1, dots, c_m$ lying in $K$.
  Moreover, for each $c_i$, we can write
  $
    c_i = sum_(j=1)^n d_(i j) v_j
  $
  for some $d_(i j)$ lying in $F$.
  This shows that 
  $
    alpha = sum_(i=1)^m sum_(j=1)^n d_(i j) u_i v_j,
  $
  which shows that $B$ generates $L$ over $F$.
  To show that $B$ is linearly independent over $F$, suppose that we have a linear combination
  $
    sum_(i=1)^m sum_(j=1)^n e_(i j) u_i v_j = 0
  $
  for some $e_(i j)$ lying in $F$.
  Then we can rewrite this as
  $
    sum_(i=1)^m (sum_(j=1)^n e_(i j) v_j) u_i = 0.
  $
  Since ${u_1, u_2, dots, u_m}$ is linearly independent over $K$, we must have
  $
    sum_(j=1)^n e_(i j) v_j = 0
  $
  for each $i = 1, dots, m$.
  Since ${v_1, v_2, dots, v_n}$ is linearly independent over $F$, we must have $e_(i j) = 0$ for all $i, j$. This shows that $B$ is linearly independent over $F$, and hence it is a basis of $L$ over $F$. Therefore, we have
  $
    [L : F] = |B| = m n = [L : K] [K : F].
  $
]

#exer[
  If an extension has prime degree, show that it has no proper intermediate extensions.
]

#lemma[
  Let $L slash K$ be a field extension, and let $alpha_1, alpha_2, dots, alpha_n in L$. Then the extension $K(alpha_1, alpha_2, dots, alpha_n) slash K$ is finite if and only if each of the extensions $K(alpha_i) slash K$ is finite for $i = 1, dots, n$.
  Moreover, if these extensions are finite, then we have
  $
    [K(alpha_1, alpha_2, dots, alpha_n) : K]
    lt.eq product_(i=1)^n [K(alpha_i) : K]
    .
  $

]

== Algebraic elements and algebraic extensions

#exer[
  Let $L slash K$ be a field extension, and let $alpha in L$. 
  
  - Show that 
    the multiplication by $alpha$ map, given by
    $
      L arrow L, quad  x mapsto alpha x,
    $
    defines a $K$-linear transformation of $L$ as a vector space over $K$.
  - 
    If $L slash K$ is a finite extension, the characteristic polynomial of this linear transformation is a monic polynomial in $K[x]$ of degree $[L : K]$
    vanishing at $alpha$.

  - 
    Assume that $alpha$ is algebraic over $K$, and $L = K(alpha)$. 
    Prove that the characteristic polynomial of 
    this linear transformation is equal to the minimal polynomial of $alpha$ over $K$.
]

#defn[
  Let $L slash K$ be a field extension. An element $alpha in L$ is said to be *algebraic* over $K$ if there exists a non-zero polynomial $f(x) in K[x]$ such that $f(alpha) = 0$. If no such polynomial exists, we say that $alpha$ is *transcendental* over $K$.
]

#exer[
  Is it true that algebraic extensions are finitely generated? If yes, prove it. If not, give a counterexample.
]

#corollary[
  Let $L slash K$ be a field extension,
  and let $alpha$ be an element of $L$. Then
  the following statements are equivalent.
  - The extension $K(alpha) slash K$ is finite.
  - The element $alpha$ is algebraic over $K$.
  Moreover, $alpha$ is algebraic over $K$ if and only if $alpha^n$
  is algebraic over $K$ for some positive integer $n$.
]

#defn[
  Let $L slash K$ be a field extension. If an element $alpha in L$ is algebraic over $K$, then the *minimal polynomial* of $alpha$ over $K$ is the unique monic polynomial $f(x) in K[x]$ of least degree such that $f(alpha) = 0$.
]

#lemma[
  Let $L slash K$ be a field extension, and let $alpha in L$ be algebraic over $K$. Then the following statements hold.
  - The minimal polynomial of $alpha$ over $K$ is irreducible in $K[x]$.
  - If $f(x) in K[x]$ is any polynomial such that $f(alpha) = 0$, then the minimal polynomial of $alpha$ over $K$ divides $f(x)$ in $K[x]$.
  - The degree of the extension $K(alpha) slash K$ is equal to the degree of the minimal polynomial of $alpha$ over $K$.
  - We have 
  $
    K(alpha) = K[alpha].
  $
]

#lemma("Finite extensions are algebraic")[
  Let $L slash K$ be a field extension.
  If $L slash K$ is a finite extension, then 
  $L$ is algebraic over $K$,
  and 
  it is finitely generated as a field extension of $K$.
]

#proposition[
  Let $L slash K$ be a field extension, and let $X$ be a subset of $L$. 
  Assume that every element of $X$ is algebraic over $K$. Then the extension $K(X) slash K$ is algebraic.
  Moreover, if $X$ is finite, then the extension $K(X) slash K$ is finite.
]

#thm[
  Let $L slash K$, $K slash F$ be field extensions. 
  If $L slash K, K slash F$ are algebraic extensions, then so is $L slash F$.
]

#lemma[
  Let $L slash K$ be a field extension. The set of all elements of $L$ that are algebraic over $K$ forms a subfield of $L$, 
  and it is the largest algebraic extension of $K$ contained in $L$.
]

// #proof[
//   Let $alpha, beta in L$ be algebraic over $K$. 
// ]

#defn[
  Let $L slash K$ be a field extension. 
  The *algebraic closure* of $K$ in $L$ is the set of all elements of $L$ that are algebraic over $K$. 
  The field extension $L slash K$ is called an *algebraic extension* if every element of $L$ is algebraic over $K$. 
]

#exer[
  Let $overline(QQ)$ denote the algebraic closure of $QQ$ in $CC$. 
  Show that $overline(QQ)$ contains an extension of $QQ$ of degree $n$ for every positive integer $n$. 
  Using this, show that $overline(QQ)$ is an infinite extension of $QQ$.
]

== Compositum of field extensions

#defn[
  Let $L_1 slash F$ and $L_2 slash F$ be field extensions, contained in a common extension $K$ of $F$. The *compositum* of $L_1$ and $L_2$ over $F$, denoted by $L_1 L_2$, is defined to be the smallest subfield of $K$ that contains both $L_1$ and $L_2$. In other words, $L_1 L_2$ is the intersection of all subfields of $K$ that contain both $L_1$ and $L_2$.
  The compositum $L_1 L_2$ is also called the *composite field* of $L_1$ and $L_2$ over $F$.
]

#exer[
  If $L_1 slash F$ and $L_2 slash F$ are finite extensions contained in a common extension $K$ of $F$, and if 
  $
    L_1 = F(alpha_1, alpha_2, dots, alpha_m),
    quad
    L_2 = F(beta_1, beta_2, dots, beta_n),
  $
  then show that
  $
    L_1 L_2 = F(alpha_1, alpha_2, dots, alpha_m, beta_1, beta_2, dots, beta_n).
  $
]

#exer[
  Show that if $L_1 slash F$ and $L_2 slash F$ are finite extensions contained in a common extension $K$ of $F$, then the compositum $L_1 L_2 slash F$ is also a finite extension of $F$, and we have
  #eqn[
    $
      [L_1 L_2 : F] lt.eq [L_1 : F] [L_2 : F].
    $
    <eqn-degree-compositum>
  ]
  Provide an example of two finite extensions $L_1 slash F$ and $L_2 slash F$ such that the inequality @eqn-degree-compositum is strict.
  Moreover, if $[L_1 : F]$ and $[L_2 : F]$ are coprime, then we have
  $
    [L_1 L_2 : F] = [L_1 : F] [L_2 : F].
  $
]

== Automorphisms of field extensions

#defn[
  Let $L slash K$ be a field extension. The set of all $K$-automorphisms of $L$, denoted by $#math.op("Gal") (L slash K)$, is called the *Galois group* of $L$ over $K$, and is defined as the set of all field automorphisms of $L$ that fix $K$ pointwise. 
]

#exer[
  Show that $#math.op("Gal") (L slash K)$ is a group under composition of maps.
]

#lemma[
  Let $L slash K$ be a field extension, and let $X$ be a subset of $L$
  such that $L = K(X)$. Show that any $K$-automorphism of $L$ is uniquely determined by its action on the elements of $X$,
  that is, if $sigma, tau$ are $K$-automorphisms of $L$ such that $sigma(x) = tau(x)$ for all $x in X$, then $sigma = tau$.
]

#lemma[
  Let $L slash K$ be a field extension, and let $alpha$ be an element of $L$ that is algebraic over $K$. Show that any $K$-automorphism $sigma$ of $L$ maps $alpha$ to a root of the minimal polynomial of $alpha$ over $K$,
  and $sigma(alpha)$ is also algebraic over $K$ with the same minimal polynomial as $alpha$.
]

#corollary[
  Let $L slash K$ be a field extension of finite degree.
  Then $#math.op("Gal") (L slash K)$ is a finite group.
]

#exer[
  Determine the Galois group of the following field extensions.
  - $QQ(sqrt(2)) slash QQ$.
  - $QQ(sqrt(2), sqrt(3)) slash QQ$.
  - $QQ(sqrt(2), root(3, 3)) slash QQ$.
  - $QQ(sqrt(2), sqrt(3), sqrt(5)) slash QQ$.
  - $QQ(root(3, 3)) slash QQ$.
  - $QQ(i) slash QQ$.
  - $C slash RR$.
  - $k(t) slash k(t^2)$ where $k$ is a field.
]

#exer[
  Let $k$ be a field. 
  - Determine whether $k[t] slash (t^2 + 1)$ is a field. If it is a field, determine its Galois group over $k$.
  - Determine whether $k[t] slash (t^2 + t + 1)$ is a field. If it is a field, determine its Galois group over $k$.
]

#remark[
  Let $K slash F$ be a field extension, and let $L$ be an intermediate extension of $K slash F$. 
  Then the Galois group of $K$ over $L$ 
  is a subgroup of the Galois group of $K$ over $F$.
]

#defn[
  Let $K slash F$ be a field extension, and let $L$ be an intermediate extension of $K slash F$. 
  If $H$ is a subgroup of the Galois group of $K$ over $F$, then the *fixed field* of $H$, 
  is denoted by $K^H$, and is defined to be the set of all elements of $K$ that are fixed by every automorphism in $H$.
  For any subset $S$ of $#math.op("Gal") (K slash F)$, we define the *fixed field* of $S$ to be
  $
    K^S = {x in K : sigma(x) = x #text[for all] sigma in S}.
  $
]

#exer[
  Show that the fixed field $K^H$ of a subgroup $H$ of the Galois group of $K$ over $F$ is an intermediate extension of $K slash F$.
  For any subset $S$ of $#math.op("Gal") (K slash F)$, show that the fixed field $K^S$ is equal to the intermediate extension $K^(chevron.l S chevron.r)$ of $K slash F$,
  where $chevron.l S chevron.r$ denotes the subgroup of $#math.op("Gal") (K slash F)$ generated by $S$.
]

Thus far we have seen that the Galois group $#math.op("Gal") (K slash F)$ of a field extension $K slash F$ is a group, and the fixed field $K^H$ of a subgroup $H$ of $#math.op("Gal") (K slash F)$ is an intermediate extension of $K slash F$,
and we have also seen that the Galois group of $K$ over an intermediate extension $L$ is a subgroup of $#math.op("Gal") (K slash F)$.
// In fact, there is a one-to-one correspondence between the subgroups of the Galois group and the intermediate extensions of $K slash F$, which is known as the *Fundamental Theorem of Galois Theory*.

#exer[
  Determine the Galois group of the extension $QQ(sqrt(2), root(3, 3)) slash QQ$ and its subgroups, and determine the corresponding intermediate extensions of $QQ(sqrt(2), root(3, 3)) slash QQ$.
  Are there more intermediate extensions than subgroups of the Galois group?
]

#exer[
  Are there similar examples in positive characteristic?
]

#exer[
  Are there more intermediate extensions than subgroups of the Galois group for the extension $QQ(sqrt(2), sqrt(3)) slash QQ$?
]

#lemma[
  Let $K slash F$ be a field extension. Then the following statements hold.
  -  
    The map
    $
      {L colon L #text[is a subextension of ] K slash F}
      arrow
      {H colon H #text[is a subgroup of ] #math.op("Gal") (K slash F)}
      ,
    $
    given by 
    $
      L arrow.r.long.squiggly #math.op("Gal") (K slash L),
    $
    is inclusion-reversing, that is, if $L_1, L_2$ are intermediate extensions of $K slash F$ such that $L_1 subset.eq L_2$, then we have
    $
      #math.op("Gal") (K slash L_2) subset.eq #math.op("Gal") (K slash L_1).
    $

  -
    The map
    $
      {L colon L #text[is a subextension of ] K slash F}
      arrow.l
      {H colon H #text[is a subgroup of ] #math.op("Gal") (K slash F)},
    $
    given by
    $
      K^H arrow.l.long.squiggly H,
    $
    is also inclusion-reversing, that is, if $H_1, H_2$ are subgroups of $#math.op("Gal") (K slash F)$ such that $H_1 subset.eq H_2$, then we have
    $
      K^(H_1) supset.eq K^(H_2).
    $
  - 
    For any intermediate extension $L$ of $K slash F$, we have
    $
      L subset.eq K^(#math.op("Gal") (K slash L)).
    $
    In particular, for any subgroup $H$ of $#math.op("Gal") (K slash F)$, we have
    $
      K^H = K^(#math.op("Gal") (K slash K^H)).
    $
  - 
    For any subset $S$ of $#math.op("Gal") (K slash F)$, we have
    $
      S subset.eq #math.op("Gal") (K slash K^(S)).
    $
    In particular, for any intermediate extension $L$ of $K slash F$, we have
    $
      #math.op("Gal") (K slash L) = #math.op("Gal") (K slash K^(#math.op("Gal") (K slash L))).
    $
]
// <lemma-Galois-correspondence>

#corollary[
  Let $K slash F$ be a field extension.
  Then the maps
  $
    L arrow.r.long.squiggly #math.op("Gal") (K slash L),
    quad
    H arrow.r.long.squiggly K^H
  $
  provide an inclusion-reversing one-to-one correspondence between the set of all intermediate extensions of $K slash F$ 
  which are the fixed fields of subgroups of $#math.op("Gal") (K slash F)$,
  and the set of all subgroups of $#math.op("Gal") (K slash F)$
  which are the Galois groups of $K$ over intermediate extensions of $K slash F$.
]

Note that the inclusion-reversing one-to-one correspondence in 
// @lemma-Galois-correspondence 
the above lemma
is not necessarily a one-to-one correspondence between all intermediate extensions of $K slash F$ and all subgroups of $#math.op("Gal") (K slash F)$, since there may be intermediate extensions of $K slash F$ that are not fixed fields of any subgroup of $#math.op("Gal") (K slash F)$, and there may be subgroups of $#math.op("Gal") (K slash F)$ that are not Galois groups of $K$ over any intermediate extension of $K slash F$.
It is natural to ask when the above inclusion-reversing one-to-one correspondence is a one-to-one correspondence between all intermediate extensions of $K slash F$ and all subgroups of $#math.op("Gal") (K slash F)$.
A necessary condition for this to happen is that the fixed field of the Galois group $#math.op("Gal") (K slash F)$ is equal to $F$, that is, we have
$
  K^(#math.op("Gal") (K slash F)) = F.
$
This leads to the following definition.

#defn[
  Let $K$ be an algebraic extension of a field $F$. We say that $K slash F$ is a *Galois extension* if the fixed field of the Galois group $#math.op("Gal") (K slash F)$ is equal to $F$, that is, we have
  $
    K^(#math.op("Gal") (K slash F)) = F.
  $
]

Note that any field automorphism $sigma$ of $K$
can be viewed as a group homomorphism from $K^times$ to itself, where $K^times$ denotes the multiplicative group of non-zero elements of $K$. 

#defn[
  Let $G$ be a group, and let $K$ be a field. A *character* of $G$ over $K$ is a group homomorphism from $G$ to the multiplicative group $K^times$ of non-zero elements of $K$. The set of all characters from $G$ to $K$ is denoted by $#math.op("Hom") (G, K^times)$.
]

#lemma("Dedekind")[
  Let $sigma_1, dots, sigma_n$ be distinct characters of a group $G$ over a field $K$. Then the characters $sigma_1, dots, sigma_n$ are linearly independent over $K$, that is, if we have a linear combination
  $
    sum_(i=1)^n c_i sigma_i = 0
  $
  for some $c_1, dots, c_n in K$, then we must have
  $
    c_1 = c_2 = dots = c_n = 0.
  $
]

The following result is a consequence of Dedekind's lemma.

#proposition[
  Let $K slash F$ be a finite extension. Then
  the Galois group $#math.op("Gal") (K slash F)$ is a finite group, and
  its order is at most the 
  degree of the extension $K slash F$, that is, we have
  $
    |#math.op("Gal") (K slash F)| lt.eq [K : F].
  $
]

#proposition[
  Let $G$ be a finite subgroup of the group of automorphisms of a field $K$. 
  Then the order of $G$ is equal to the degree of the extension $K slash K^G$, that is, we have
  $
    |G| = [K : K^G].
  $
  Consequently, the extension $K slash K^G$ is finite and Galois, and 
  has $G$ as its Galois group, that is, we have
  $
    G = #math.op("Gal") (K slash K^G).
  $
]

#corollary[
  A finite extension $K slash F$ is Galois if and only if the order of the Galois group $#math.op("Gal") (K slash F)$ is equal to the degree of the extension $K slash F$, that is, we have
  $
    |#math.op("Gal") (K slash F)| = [K : F].
  $
]

#corollary[
  Let $K slash F$ be a field extension, and let $alpha in K$ be algebraic over $F$.
  Then the order of the Galois group $#math.op("Gal") (F(alpha) slash F)$ is equal to 
  the number of distinct roots of the minimal polynomial of $alpha$ over $F$ in $F(alpha)$.
  Consequently, the extension $F(alpha) slash F$ is Galois if and only if 
  the number of distinct roots of the minimal polynomial of $alpha$ over $F$ in $F(alpha)$ is equal to 
  the degree of the extension $F(alpha) slash F$.
]

#exer[
  Determine the Galois group of the extension $QQ(root(3, 3)) slash QQ$ and its subgroups, and determine the corresponding intermediate extensions of $QQ(root(3, 3)) slash QQ$.
]

#exer[
  Similar problem as the previous exercise, but for the extension $k(t) slash k(t^2)$, 
  or for the extension $k(t) slash k(t^p)$ for any prime $p$ and any field $k$ of characteristic $p$.
]
