function [NextGen numMutations] = mutate(mutationProb, NextGen)

numChromosomes = length(NextGen(:,1));
numCities = length(NextGen(1,:))-2;

probs = rand(numChromosomes, numCities);
swaps = probs < mutationProb;
numMutations = zeros(1, numChromosomes);
for i = 1:numChromosomes
    mutationCount = 0;
    if sum(swaps(i,:)) > 1
        swap_index = find(swaps(i,:));
        for j = 1:length(swap_index)-1
            mutationCount = mutationCount + 1;
            save = NextGen(i,swap_index(j)+1); 
            NextGen(i,swap_index(j)+1) = NextGen(i,swap_index(j+1)+1);
             NextGen(i,swap_index(j+1)+1) = save;
        end
        numMutations(i) = mutationCount;
    end
end
