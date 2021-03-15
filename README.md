# Assignment1
# In this assingment, I will follow , which deals with constructing a 'balanced' basket to hedge away risks exposed to its legs. In the article, the author proposed several methods to create such baskets, and I will implement some of them in Python.

## 1.Main Problem
Suppose we have n instruments to create a porfolio, we have their convaiance matrix V and weights on each instruments w, a most common way to construct a basket is to minimize its variance subject to the asset already in hold, that is $min x'Vw, subject to w_1=h_1$  
 
 
