function indexesForBreeding = find_fittest(scoreProb, numChildren)

children_count = 0;
scoresCDF(1) = 0;
for i = 2:length(scoreProb)+1
    scoresCDF(i) = scoresCDF(i-1) + scoreProb(i-1);
end

while (children_count < numChildren)
    prob = rand(1);
    for j = 2:length(scoresCDF)
        if  (scoresCDF(j-1) <= prob) & (scoresCDF(j) >= prob)  
            children_count = children_count + 1;
            indexesForBreeding(children_count) = j-1;
%             scoreProb(j) = 0;
            break;
        end
    end
end
    
    