function Offspring = breed(route, indexesForBreeding)

numChildren = length(indexesForBreeding)-1;
numCities = length(route(1,:)) - 2;
Offspring = zeros(numChildren, numCities+2);
    Offspring(:,1) = route(1:numChildren,1);
    Offspring(:,end) = route(1:numChildren,end);
for i = 1:numChildren
    child_index1 =1; child_index2 = 1;
    while(indexesForBreeding(child_index1) == indexesForBreeding(child_index2))
        child_index1 = ceil(numChildren*rand(1));
        child_index2 = ceil(numChildren*rand(1));
    end
    parent1 = route(indexesForBreeding(child_index1),2:end-1);
    parent2 = route(indexesForBreeding(child_index2),2:end-1);
    

    
    index1 = ceil(numCities * rand(1));
    index2 = ceil(numCities * rand(1));

    if index1 > index2
        save = index1;
        index1 = index2;
        index2 = save;
    end
    
    index = 1;
    for j = 1:length(parent2)
        if (ismember(j, index1:index2))
            Offspring(i,j+1) = parent1(j);
        else
            while((ismember(parent2(index),parent1(index1:index2))))
                index = index + 1;
            end
            Offspring(i,j+1) = parent2(index);
            index = index + 1;
        end
    end
end

                