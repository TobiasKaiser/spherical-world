Flat 2D space
=============

Let us look at flat two-dimensional as a simple example to get familiar with a simple geometry and movement through spaces.

We will define flat 2D space as

.. math::

    A = \left\{ (x, y, 1) \ \mid x, y \in \mathbb{R} \right\} \subset \mathbb{R}^3.


We use a "light version" of `homogenous coordinates`_ with the third dimension fixed to one here. This leads us to the Euclidean group of 2D space without much effort and allows us to follow a top-down approach. It also familiarizes ourselves with homogenous coordinates, which are heavily used in computer graphics.

.. _homogenous coordinates: https://en.wikipedia.org/wiki/Homogeneous_coordinates

We can express transformations of a point :math:`(x, y, 1)` by multiplication it with an arbitrary :math:`3 \times 3` matrix from the left:

.. math::

    \begin{pmatrix} M_{11} & M_{12} & M_{13} \\ M_{21} & M_{22} & M_{23} \\ M_{31} & M_{32} & M_{33}\\\end{pmatrix} 
    \begin{pmatrix}x\\y\\1\\\end{pmatrix}
    = \begin{pmatrix}M_{11}x + M_{12}y + M_{13}\\M_{21}x + M_{22}y + M_{23}\\M_{31}x + M_{32}y + M_{33}\\\end{pmatrix}
    

Affine group Aff(2, R)
----------------------

We are now interested in all matrices that map arbitrary points in A to other points in A, or in other words all matrices under which the set :math:`A` is closed.

This closure requires the last dimension of the resulting vector to be one for any :math:`x` and :math:`y`:

.. math::
    M_{31}x + M_{32}y + M_{33} = 1

Setting :math:`M_{31}` or :math:`M_{32}` to anything other than zero means that the left side of the equation becomes zero for some :math:`x, y`. The only possible option is :math:`\\M_{31} = M_{32} = 0, M_{33} = 1`. 

The affine group :math:`\mathit{Aff}(2, \mathbb{R})` consists of all invertible :math:`3 \times 3` matrices that satisfy the closure requirement introduced above:

.. math::
    \mathit{Aff}(2, \mathbb{R}) = \left\{ M = \begin{pmatrix} M_{11} & M_{12} & M_{13} \\ M_{21} & M_{22} & M_{23} \\ 0 & 0 & 1\\\end{pmatrix} \mid M_{ij} \in \mathbb{R}, \det M \neq 0 \right\}

:math:`\mathit{Aff}(2, \mathbb{R})` is a subgroup of the general linear group :math:`GL(3, \mathbb{R})`.


Special Euclidean group SE(2)
-----------------------------

We want to impose two additional restrictions on the set on matrices that we are interested in:

- isometry: the matrix should preserve distances
- preservation of handedness: a left hand should remain a left hand, a clock-wise angle should remain a clock-wise angle, no mirroring allowed.
  

