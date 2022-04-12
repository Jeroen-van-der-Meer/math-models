# embedding-points

Let us consider an abstract collection of points, say x<sub>0</sub> through x<sub>n</sub>. The only thing we know about the points is their mutual distances &mdash; say, the distance between x<sub>i</sub> and x<sub>j</sub> is d<sub>ij</sub>. Is there a way to realise these points in some Euclidean space R<sup>3</sup> so that the prescribed distances are precisely the Euclidean distances?

An obvious first constraint is that the d<sub>ij</sub> satisfy the usual properties of metrics: symmetry and the triangle inequality. But this turns out not to be sufficient; as an illustration, consider the 4 points with prescribed distance matrix

    D = 0 1 3 4
        1 0 2 t
        3 2 0 5
        4 t 5 0

The value of t is completely determined because the first three points are forced to be collinear. (The value is &#x221A;17.) Yet triangle inequalities only let you infer that t lies between 3 and 5! Clearly, then, an additional obstruction is needed. Let's consider an example.

Denote, as before, by d<sub>ij</sub> the specified distance between x<sub>i</sub> and x<sub>j</sub>. Then an elementary calculation will show you that

    x_i · x_j = d_{0i}^2 + d_{0j}^2 - d_{ij}^2,

where · denotes the dot product between x<sub>i</sub> and x<sub>j</sub>. Now define the (n - 1) x (n - 1) matrix C as

    C_{ij} = d_{0i}^2 + d_{0j}^2 - d_{ij}^2,

and define the (n - 1) x 3 matrix X as

    X = (x_0 x_1 ··· x_n).

Then we can rewrite the dot product identity simply as

    X^T X = C.

What this immediately tells you is that the matrix C must have rank equal to 3 &mdash; a fact not at all obvious from its definition. This observation is known as Schoenberg's criterion.

What's truly powerful about this criterion is that it also suggests a way to find approximate embeddings: If we're given an abstract collection of points with prescribed distances d<sub>ij</sub>, then how can we embed the points in R<sup>3</sup> so as to most faithfully preserve their prescribed distances? The key is to consider the best possible approximation of C by a rank-3 matrix! And this we can do easily with a simple PCA-based dimensionality reduction. Implementation of this idea is the goal of this notebook.
