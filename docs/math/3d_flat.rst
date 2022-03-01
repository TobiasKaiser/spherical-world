Flat 3D space
=============

Flat, three-dimensional space is what we experience in everyday life. All vectors of three real numbers (:math:`\mathbb{R}^3`) represent distinct points of this space.

A lot of math is conveniently easy in this type of space. The distance between two points

.. math::

    p = \begin{pmatrix}p_\mathrm{x}\\p_\mathrm{y}\\p_\mathrm{z}\\\end{pmatrix} \in \mathbb{R}^3, q = \begin{pmatrix}q_\mathrm{x}\\q_\mathrm{y}\\q_\mathrm{z}\\\end{pmatrix} \in \mathbb{R}^3

can be calculated as

.. math::
    
    \| q - p \| = \sqrt{(p_\mathrm{x} - q_\mathrm{x})^2 + (p_\mathrm{y} - q_\mathrm{y})^2 + (p_\mathrm{z} - q_\mathrm{z})^2}.


Isometries of R3
----------------

The isometries of R3 are all transformations :math:`M: \mathbb{R}^3 \to \mathbb{R}^3` that preseve distances between all points:

.. math::

    \| M(q) - M(p) \| = q - p

Permutations of coordinate axes are isometries, for example:

.. math::

    M(p) = \begin{pmatrix}p_\mathrm{y}\\p_\mathrm{x}\\p_\mathrm{z}\\\end{pmatrix}

Flipping signs is also okay:

.. math::

    M(p) = \begin{pmatrix}-p_\mathrm{x}\\p_\mathrm{y}\\-p_\mathrm{z}\\\end{pmatrix}

Distances are also preseved if we add fixed values to each point. This is called translation. Example:

.. math::

    M(p) = p + \begin{pmatrix}9\\12\\-50\\\end{pmatrix}

The Euclidean group E(3)
------------------------

The Euclidean group :math:`E(3)` contains all isometries of :math:`\mathbb{R}^3`. Therefore, :math:`\mathbb{E}^3` is the isometry group of R3. It includes all possible rotations, translations, and mirror reflections in flat 3D space.

The spcial Euclidean group :math:`SE(3) \subset E(3)` furthermore excludes mirror reflections (preserves handedness). :math:`SE(3)` covers all translational and rotational degrees of freedom in 3D space. :math:`SE(3)` is six-dimensional.

The elements of :math:`SE(3)` can be described as combination of orthogonal (rotation) matrices and translation vectors:

.. math::

    SE(3) = \left\{ (R, t) \mid R \in \mathbb{R}^{3 \times 3}, \det R = 1, t \in \mathbb{R}^3 \right\}

They act on :math:`\mathbb{R}^3` with matrix multiplication followed by addition:

.. math::

    p \mapsto Rp + t

Generally, this action is not a linear transformation but only an affine transformation, since the origin is not preserved if :math:`t` is not zero.

:math:`SE(3)` can also be secribed as set of 4D matrices that encapsulate rotation matrix and translation  vector:

.. math::

    SE(3) = \left\{ \begin{pmatrix}R_{11}&R_{12}&R_{13}&t_{x}\\R_{21}&R_{22}&R_{23}&t_{y}\\R_{31}&R_{32}&R_{33}&t_{z}\\0&0&0&1\\\end{pmatrix} \mid R = \begin{pmatrix}R_{11}&R_{12}&R_{13}\\R_{21}&R_{22}&R_{23}\\R_{31}&R_{32}&R_{33}\\\end{pmatrix} \in \mathbb{R}^{3 \times 3}, \det R = 1, t = \begin{pmatrix}t_\mathrm{x}\\t_\mathrm{y}\\t_\mathrm{z}\\\end{pmatrix} \in \mathbb{R}^3 \right\}    

With this, the action on :math:`\mathbb{R}^3` can be reduced to a single matrix multiplication:

.. math::

    p \mapsto R \cdot \begin{pmatrix}-p_\mathrm{x}\\p_\mathrm{y}\\-p_\mathrm{z}\\1\\\end{pmatrix}

We can either let the number 1 in the fourth dimension of our vector appear here out of nowhere, or we can switch to using 4D vectors with a fixed 1 in the fourth dimension. Using such 4D vectors makes it also possible to distinguish between absolute points (with a 1 in the fourth dimension) and relative vectors (with a 0 in the fourth dimenion). You can see that the fourth, translational column of the :math:`4 \times 4` matrix is now only applied to absolute points, preserving the lengths of relative vectors.

More resources to this can be found under the keywords affine space and affine transformations.

Unusual but hopefully demonstrative: We can interpret flat 3D space as being embedded in :math:`\mathbb{R}^4` with the origin of flat 3D space :math:`(0, 0, 0, 1)` being the closest point to the 4D origin :math:`(0, 0, 0, 0)` with a distance of one. (The fourth dimension will be called :math:`w`.)

Interesting, but probably not useful: The points in this embedded flat 3D space with a particular distance :math:`d > 1` from the 4D origin form a sphere (2-sphere) of radius :math:`\sqrt{d^2 - 1}` in the embedded 3D space.

Quaternion trickery for 3D rotation
-----------------------------------

Do we need angles?
------------------

The angle :math:`\theta` between two can be found using the dot product:

.. math::

    \| p \| \cdot \| q \| \cdot \cos \theta = p \cdot q = ( p_\mathrm{x} \cdot q_\mathrm{x} + p_\mathrm{y} \cdot q_\mathrm{y} + p_\mathrm{z} \cdot q_\mathrm{z} )
