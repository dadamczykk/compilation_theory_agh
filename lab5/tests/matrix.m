A = eye(3);
B = ones(3);
C = A .+ B;
print C;

D = zeros(3, 4);
D[0, 0] = 42;
D[2,2] = 5;
D[1:3, 2:4] = 7;
print D;
print D[2, 2];

ala = A .- [3, 2.7, 1];

ela = [[1, 2], [2, 2]] .* [[3, 3], [4, 4]];

print ala, ela;
