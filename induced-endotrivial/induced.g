InduceRepresentation := function(G, rep)
#Given a representation rep : H -> GL_n and a supergroup G, compute the induced representation Ind^G(M)
	local H, index, range, generators, images, cosets, blocks, image_of_g, i, j, g, x;
	H := Source(rep);
	index := Index(G, H);
	range := GeneralLinearGroup(index * DimensionOfMatrixGroup(Range(rep)), DefaultFieldOfMatrixGroup(Range(rep)));
	generators := GeneratorsOfGroup(G); #This is the target of the induced representation
	images := [ ]; #These will describe the images of the generators of G under the induced representation
	cosets := RightTransversal(G, H);

	#An induced representation can be represented in terms of block matrices
	#In the code below we construct these block matrices
	for g in GeneratorsOfGroup(G) do
		#Build up the block matrix of the image of g
		blocks := [ ];
		for i in [1..index] do
			for j in [1..index] do
				x := cosets[i]^(-1) * g * cosets[j];
				if x in H then
					Add(blocks, [i, j, Image(rep, x)]);
				fi;
			od;
		od;
		image_of_g := BlockMatrix(blocks, index, index);
		Add(images, image_of_g);
	od;
	return GroupHomomorphismByImages(G, range, generators, images);
end;

InternalHom := function(rep1, rep2)
#Given two representations rep_i : G -> GL_n, compute their internal Hom
#To go about this, recall that Hom(M, N) is isomorphic to M* otimes N
	local G, range, generators, images, g, image_of_g;
	G := Source(rep1);
	range := GeneralLinearGroup(DimensionOfMatrixGroup(Range(rep1)) * DimensionOfMatrixGroup(Range(rep2)), DefaultFieldOfMatrixGroup(Range(rep1)));
	generators := GeneratorsOfGroup(G);
	images := [ ]; #Images of generators of G under the internal Hom representation
	for g in generators do
		#Build up the images of the generators of G
		image_of_g := KroneckerProduct(TransposedMat(Image(rep1, g^(-1))), Image(rep2, g));
		Add(images, image_of_g);
	od;
	return GroupHomomorphismByImages(G, range, generators, images);
end;
