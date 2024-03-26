
%%%%%%%%%%%%%%%%%%%%%%
%%    KEY SCRIPT    %%
%%%%%%%%%%%%%%%%%%%%%%
%v1.0 11/10/2022
%Analyses of the particles movement
%MSD analyses 

close all; clear 
set(0,'DefaultFigureWindowStyle','docked')

%Toolbox
%https://sbalzarini-lab.org/MosaicSuiteDoc/install.html
%Tutorial
%https://sbalzarini-lab.org/MosaicToolboxSuite/ParticleTracker.html

%Acquisition parameters
res=[0.2513,0.2513]; %microscope resolution in micrometer, x,y
dT=0.25;  %Time steps in sec

%%
%Input files
base_win='D:\COLLABS\cilia_fanny\data\beads_curated\';
base=base_win; 

%Heterozygous triple mutants 
path{1}=[base 'het-beads-0.25s-01_traj.txt'];  
path{2}=[base 'het-beads-0.25s-02_traj.txt']; 
path{3}=[base 'het-beads-0.25s-05_traj.txt']; 
path{4}=[base 'het-beads-0.25s-06_traj.txt']; 
path{5}=[base 'het-beads-0.25s-07_traj.txt']; 
%Triple
path{6}=[base 'trip-beads-0.25s-01_traj.txt'];
path{7}=[base 'trip-beads-0.25s-02_traj.txt'];
path{8}=[base 'trip-beads-0.25s-03_traj.txt'];
%WT
path{9}=[base 'wt-beads-0.25s-02_traj.txt'];
path{10}=[base 'wt-beads-0.25s-03_traj.txt'];
path{11}=[base 'wt-beads-0.25s-04_traj.txt'];

%% 
%Initialize arrays
trajspeedHet=[];
trajspeedTrip=[];
trajspeedWT=[];

for file_idx=1:length(path)

    %Extract trajectories
    all_text = readlines(path{file_idx}); matches = regexp(all_text,'Trajectory');
    idx_trajs=find(~cellfun(@isempty,matches));
    clear traj
    for idx_traj=2:length(idx_trajs)
        if idx_traj<length(idx_trajs)
            onsetline=idx_trajs(idx_traj)+2; offsetline=idx_trajs(idx_traj+1)-2;
            lines=onsetline:offsetline;
            for idx_time=1:length(lines)
                str = split(all_text(lines(idx_time)),' ');
                traj{idx_traj-1}.posT(idx_time)=str2num(str(1));
                traj{idx_traj-1}.posX(idx_time)=str2num(str(2))*res(1);
                traj{idx_traj-1}.posY(idx_time)=str2num(str(3))*res(2);
            end
        elseif idx_traj==length(idx_trajs)
            onsetline=idx_trajs(idx_traj)+2; offsetline=length(all_text)-2;
            lines=onsetline:offsetline;
            for idx_time=1:length(lines)
                str = split(all_text(lines(idx_time)),' ');
                traj{idx_traj-1}.posT(idx_time)=str2num(str(1));
                traj{idx_traj-1}.posX(idx_time)=str2num(str(2))*res(1);
                traj{idx_traj-1}.posY(idx_time)=str2num(str(3))*res(2);
            end
        end
        trajsteps(idx_traj-1)=length(traj{idx_traj-1}.posT);
        trajdistance(idx_traj-1)=sum(sqrt(diff(traj{idx_traj-1}.posX*res(1)).^2+diff(traj{idx_traj-1}.posY*res(2)).^2));
        trajspeed(idx_traj-1)=trajdistance(idx_traj-1)/(trajsteps(idx_traj-1)*dT); %in um/sec
    end
    
    %Store for histrogram plot
    %Hets
    if ismember(file_idx, [1 2 3 4 5])
        trajspeedHet=[trajspeedHet trajspeed]; 
        %Triple
    elseif ismember(file_idx, [6 7 8])
        trajspeedTrip=[trajspeedTrip trajspeed]; 
        %WT
    elseif ismember(file_idx, [9 10 11])
        trajspeedWT=[trajspeedWT trajspeed]; 
    end

    %%
    %With colors changing with time
    %Colobar saturating at 20 secs.
    segColors = parula(10); %color change in the first 20 segments only
    for col_idx=11:500
        segColors(col_idx,:)=[0.9769 0.9839 0.0805]; %yellow at the end
    end
    
    %Plot each trajectories
    figure; set(gcf,'color','w');
    for idx_traj=1:length(traj)
        
        %Keep only trajectories with at least 4 points
        if trajsteps(idx_traj)>prctile(trajsteps,80)
            x=traj{idx_traj}.posX'; y=traj{idx_traj}.posY';
            
            %Cut into segments
            xseg = [x(1:end-1),x(2:end)]; yseg = [y(1:end-1),y(2:end)];
            
            %Plot
            h = plot(xseg',-yseg','-','LineWidth',4,'Visible','Off');
            axis equal;
            
            % Adapt colormap and set colors
            segColorsTemp = segColors(1:size(xseg,1),:);
            set(h, {'Color'}, mat2cell(segColorsTemp,ones(size(xseg,1),1),3))
            set(h, 'Visible', 'on')
            hold on
        end
    end
    axis square; 
    xlabel('Distance (um)'); ylabel('Distance (um)')
    
    %Colorbar
    ticks=[0:9]*dT; toptick=10*dT; 
    c=colorbar('XTickLabel',[num2cell(ticks) ['>' num2str(toptick)]]); 
    c.Label.String = 'Time (sec)';  c.LineWidth=2; 
    %General behavior
    set(findall(gcf,'-property','FontSize'),'FontSize',16)
    set(gca,'linewidth',2)
    %Export figure 
    filename=[path{file_idx}(1:end-4) '.pdf']; 
    %exportgraphics(gcf,filename,'ContentType','vector')
end

%%
%MSD Analysis @msdanalyzer
%Using this excellent tutorial: http://tinevez.github.io/msdanalyzer/tutorial/MSDTuto_brownian.html
%Trajectories >1 sec tracking and <8sec

%Extract WT trajectories
idx_traj_glob=0; 
for file_idx=9:11
    all_text = readlines(path{file_idx}); matches = regexp(all_text,'Trajectory');
    idx_trajs=find(~cellfun(@isempty,matches));
    clear trajWT
    for idx_traj=2:length(idx_trajs)
        idx_traj_glob=idx_traj_glob+1; 
        if idx_traj<length(idx_trajs)
            onsetline=idx_trajs(idx_traj)+2; offsetline=idx_trajs(idx_traj+1)-2;
            lines=onsetline:offsetline;
            for idx_time=1:length(lines)
                str = split(all_text(lines(idx_time)),' ');
                trajWT{idx_traj-1}.posT(idx_time)=str2num(str(1));
                trajWT{idx_traj-1}.posX(idx_time)=str2num(str(2))*res(1);
                trajWT{idx_traj-1}.posY(idx_time)=str2num(str(3))*res(2);
            end
        elseif idx_traj==length(idx_trajs)
            onsetline=idx_trajs(idx_traj)+2; offsetline=length(all_text)-2;
            lines=onsetline:offsetline;
            for idx_time=1:length(lines)
                str = split(all_text(lines(idx_time)),' ');
                trajWT{idx_traj-1}.posT(idx_time)=str2num(str(1));
                trajWT{idx_traj-1}.posX(idx_time)=str2num(str(2))*res(1);
                trajWT{idx_traj-1}.posY(idx_time)=str2num(str(3))*res(2);
            end
        end
        trajWTall(idx_traj_glob).posT=trajWT{idx_traj-1}.posT;
        trajWTall(idx_traj_glob).posX=trajWT{idx_traj-1}.posX;
        trajWTall(idx_traj_glob).posY=trajWT{idx_traj-1}.posY;
    end
end 
%Reformat files for @msd compliance
idx_temp=0; clear trajWTMSD
for idx_traj=1:length(trajWTall)
    temp_pos=(trajWTall(idx_traj).posT)-min(trajWTall(idx_traj).posT); 
    if length(temp_pos)>4 && length(temp_pos)<40
        idx_temp=idx_temp+1
        trajWTMSD{idx_temp,1}=[temp_pos*dT; trajWTall(idx_traj).posX; trajWTall(idx_traj).posY]';
        if idx_traj < 41
            trajWTMSDshort{idx_temp,1}=[temp_pos*dT; trajWTall(idx_traj).posX; trajWTall(idx_traj).posY]';
        end 
    end 
end

%%
% Extract Trip trajectories
idx_traj_glob=0;
for file_idx=6:8
    all_text = readlines(path{file_idx}); matches = regexp(all_text,'Trajectory');
    idx_trajs=find(~cellfun(@isempty,matches));
    clear trajTrip
    for idx_traj=2:length(idx_trajs)
        idx_traj_glob=idx_traj_glob+1;
        if idx_traj<length(idx_trajs)
            onsetline=idx_trajs(idx_traj)+2; offsetline=idx_trajs(idx_traj+1)-2;
            lines=onsetline:offsetline;
            for idx_time=1:length(lines)
                str = split(all_text(lines(idx_time)),' ');
                trajTrip{idx_traj-1}.posT(idx_time)=str2num(str(1));
                trajTrip{idx_traj-1}.posX(idx_time)=str2num(str(2))*res(1);
                trajTrip{idx_traj-1}.posY(idx_time)=str2num(str(3))*res(2);
            end
        elseif idx_traj==length(idx_trajs)
            onsetline=idx_trajs(idx_traj)+2; offsetline=length(all_text)-2;
            lines=onsetline:offsetline;
            for idx_time=1:length(lines)
                str = split(all_text(lines(idx_time)),' ');
                trajTrip{idx_traj-1}.posT(idx_time)=str2num(str(1));
                trajTrip{idx_traj-1}.posX(idx_time)=str2num(str(2))*res(1);
                trajTrip{idx_traj-1}.posY(idx_time)=str2num(str(3))*res(2);
            end
        end
        trajTripall(idx_traj_glob).posT=trajTrip{idx_traj-1}.posT;
        trajTripall(idx_traj_glob).posX=trajTrip{idx_traj-1}.posX;
        trajTripall(idx_traj_glob).posY=trajTrip{idx_traj-1}.posY;
    end
end
%Reformat files for @msd compliance
idx_temp=0; clear trajTripMSD
for idx_traj=1:length(trajTripall)
    temp_pos=(trajTripall(idx_traj).posT)-min(trajTripall(idx_traj).posT);
    if length(temp_pos)>4 && length(temp_pos)<40
        idx_temp=idx_temp+1
        trajTripMSD{idx_temp,1}=[temp_pos*dT; trajTripall(idx_traj).posX; trajTripall(idx_traj).posY]';
         if idx_traj < 50
            trajTripMSDshort{idx_temp,1}=[temp_pos*dT; trajTripall(idx_traj).posX; trajTripall(idx_traj).posY]';
        end 
    end
end

%%
%Compute and plot MSD 
%Instantiate the analyzer 
ma = msdanalyzer(2, 'µm', 's');

f1 = figure('DefaultTextFontName', 'Arial');
tiledlayout(2,2);
set(gcf,'Color','w'); 
set(0,'DefaultAxesFontName', 'FreeSans'); set(0,'DefaultAxesFontSize', 16); %Axes
set(0,'DefaultTextFontname', 'FreeSans'); set(0,'DefaultTextFontSize', 16); %Text

%WT
nexttile
maWT = ma.addAll(trajWTMSDshort); disp(maWT)
maWT.plotTracks; maWT.labelPlotTracks;  axis square
axis([10 40 10 40])
title('wt')
nexttile
maWT = ma.addAll(trajWTMSD); disp(maWT)
maWT.plotMeanMSD(gca, true); axis([0 8 0 600]); axis square
[fo, gof] = maWT.fitMeanMSD; 


%Triple mutants
nexttile
maTrip = ma.addAll(trajTripMSDshort); disp(maTrip)
maTrip.plotTracks; maTrip.labelPlotTracks; axis square
axis([20 50 20 50])
title('tripMut')
nexttile
maWT = ma.addAll(trajTripMSD); disp(maWT)
maTrip.plotMeanMSD(gca, true); axis([0 8 0 600]); axis square

exportgraphics(f1,'C:\Users\jboulanger\Dropbox (Harvard University)\collabs\cilia_fanny\msd_analysis_11012022.pdf')