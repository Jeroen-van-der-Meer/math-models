Let $H$ be the quaternion group $Q_8$. Let $M$ be the $3$-dimensional representation over $k = \mathbb{F}_4$ given by
$$ i \mapsto \begin{pmatrix} 1&0&0 \\\ 1&1&0 \\\ 0&1&1 \end{pmatrix} \qquad \text{and} \qquad j \mapsto \begin{pmatrix} 1&0&0 \\\ \omega&1&0 \\\ 0&\omega^2&1\end{pmatrix} \text{,} $$
where $\omega$ is a primitive third root of unity in $k$. $M$ is an endopermutation module, meaning that $\operatorname{End}_k(M)$ has a permutation basis. In fact,
$$ \operatorname{End}_k(M) \cong k \oplus kQ_8 \text{,} $$
which makes it an endotrivial module.

Now let $G$ be the semidihedral group $\mathrm{SD}_{16}$. $H$ is an index-$2$ subgroup of $G$ in a unique way. I claim that $\operatorname{Ind}^G_H(M)$ is no longer an endopermutation module. We will verify this directly using GAP.

We begin by loading the supplied ```induced.g``` file, which tells GAP how to compute induced modules and internal Homs.

```GAP
Read("induced.g");
```

We now realise $\mathrm{SD}_{16}$ and its subgroup $Q_8$.

```GAP
F := FreeGroup("a", "x");
SD16 := F / [F.1^8, F.2^2, F.2*F.1*F.2^(-1)*F.1^(-3)];
Q8 := Subgroup(SD16, [SD16.1^2, SD16.1*SD16.2]);
```

We set up the initial representation:
```GAP
GL3 := GeneralLinearGroup(3, GF(4));
images := [ Z(2)^0 * [[1, 0, 0], [1, 1, 0],      [0, 1, 1]       ],
            Z(2)^0 * [[1, 0, 0], [Z(2^2), 1, 0], [0, Z(2^2)^2, 1]] ];
endotrivial := GroupHomomorphismByImages(Q8, GL3, GeneratorsOfGroup(Q8), images);
```

We compute the induced representation:
```GAP
induced := InduceRepresentation(SD16, endotrivial);
hom_of_induced := InternalHom(induced, induced);
module := GModuleByMats([Image(hom_of_induced, SD16.1), Image(hom_of_induced, SD16.2)], GF(4));
```

We use the MeatAxe indecomposition function to check its indecomposable summands:
```GAP
MTX.Indecomposition(module);

[ [ < immutable compressed matrix 18x36 over GF(4) >, 
      rec( IsOverFiniteField := true, 
          basisModuleEndomorphisms := 
            [ < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) >, 
              < immutable compressed matrix 18x18 over GF(4) > ], 
          dimension := 18, field := GF(2^2), 
          generators := [ < immutable compressed matrix 18x18 over GF(4) >,
              < immutable compressed matrix 18x18 over GF(4) > ], 
          isIndecomposable := true, isMTXModule := true, 
          smashMeataxe := 
            rec( 
              basisEndoRad := 
                [ < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) >, 
                  < immutable compressed matrix 18x18 over GF(4) > ], 
              endAlgResidue := 
                [ < immutable compressed matrix 18x18 over GF(4) >, 6 ] ) 
         ) ], 
  [ < immutable compressed matrix 16x36 over GF(4) >, 
      rec( IsOverFiniteField := true, 
          basisModuleEndomorphisms := 
            [ < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) >, 
              < immutable compressed matrix 16x16 over GF(4) > ], 
          dimension := 16, field := GF(2^2), 
          generators := [ < immutable compressed matrix 16x16 over GF(4) >,
              < immutable compressed matrix 16x16 over GF(4) > ], 
          isIndecomposable := true, isMTXModule := true, 
          smashMeataxe := 
            rec( 
              basisEndoRad := 
                [ < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) >, 
                  < immutable compressed matrix 16x16 over GF(4) > ], 
              endAlgResidue := 
                [ < immutable compressed matrix 16x16 over GF(4) >, 6 ] ) 
         ) ], 
  [ < immutable compressed matrix 2x36 over GF(4) >, 
      rec( IsOverFiniteField := true, 
          basisModuleEndomorphisms := 
            [ [ [ Z(2)^0, 0*Z(2) ], [ 0*Z(2), Z(2)^0 ] ], 
              [ [ 0*Z(2), Z(2)^0 ], [ 0*Z(2), 0*Z(2) ] ] ], 
          dimension := 2, field := GF(2^2), 
          generators := [ [ [ Z(2)^0, Z(2^2)^2 ], [ 0*Z(2), Z(2)^0 ] ], 
              [ [ Z(2)^0, Z(2^2)^2 ], [ 0*Z(2), Z(2)^0 ] ] ], 
          isIndecomposable := true, isMTXModule := true, 
          smashMeataxe := 
            rec( 
              basisEndoRad := 
                [ [ [ 0*Z(2), Z(2^2)^2 ], [ 0*Z(2), 0*Z(2) ] ] ], 
              endAlgResidue := 
                [ [ [ Z(2^2)^2, Z(2)^0 ], [ 0*Z(2), Z(2^2)^2 ] ], 6 ] ) ) 
     ] ]
```

One of the indecomposable summands has dimension $18$, which directly implies that the endomorphism $G$-module isn't a permutation module. Indeed, a permutation module will always have indecomposable summands of the form $k(G/K)$ where $K$ is a subgroup of $G$, and the dimension of such summands necessarily divide the order of $G$, which is $16$.  Hence we are done.
