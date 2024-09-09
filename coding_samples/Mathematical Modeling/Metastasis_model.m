%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Modeling Tumor Substrate Consumption/Production 
% Nassima Bouhenni
% (all default values are for breast cancer data from the literature)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all

%Parameters + Variables

%Length of Tumor(um)
L = 1000;
%Nodes
N = 100; 
%Length of Diffusable Area  
H = 200;

del_x = L/N;
HN = H/del_x + N;

%Diffusion Coefficients (um^2/h)
D_O2 = 7.2e6; %(1)
D_Gl = 5.9e6; %(2)
D_La = 1.0e6; %(3)
 
%Constant Concentrations at Right Boundary L+H (g/L) 
CO2_bulk = 0.21; %(4)
CGl_bulk = 0.81; %(5)

%Cell Density (~1 cell/25 um) %(6)
cell_length = 25;
cell_density = 1/cell_length;
rho = cell_density*ones(HN, 1); 
rho(N+1:HN) = 0;

%Michaelis Menten Kinetics

%Vmax, Maximum Rate of Substrate Consumption/Production (g/L/h)
VO2 = 3744; %(7)
VGl = 135; %(8)
VLA = 42.75; %(8)
%BM2, data: VO2 = 12792 (9); VGl = 18900 (9); VLA = 11160 (9); 
%Lung, literature: VO2 = 3456 (7); VGl = 87588 (10); VLA = 2021 (11);
%LM2, data: VO2 = 29680 (9); VGl = 21420 (9); VLA = 17370 (9);
%Brain, literature: VO2 = 1344 (7); VGl = 84985(12); VLA = 4356072 (13);
%BrM2, data: VO2 = 26255 (9); VGl = 14220 (9); VLA = 12150 (9);

%Substrate Yield
YO2 = 0.5; 
YGl = 0.5; 
YLA = 0.5; 

%Half Rate of Substrate Consumption/Production (g/L/h)
RO2 = VO2*YO2; 
RGl = VGl*YGl;
RLA = VLA*YLA;

%Substrate Concentration at Half Rate (g/L)
KmO2 = 3.2e-5; %(7)
KmGl = 0.468; %(8)
KmLa = 0.243; %(8)
%Lung, literature: KmO2 = 3.2e-5 (7); KmGl = 1.3194 (10); KmLA = 0.423 (11);
%Brain, literature: KmO2 = 3.2e-5 (7); KmGl = 0.144 (12); KmLA = 0.00756 (13);

%Time Paramters

%CFL condition
t_CFL_LA = sqrt(D_La*VLA);
t_CFL_Gl = sqrt(D_Gl*VGl);
t_CFL_O2 = sqrt(D_O2*VO2);
t_CFL = max([t_CFL_LA t_CFL_Gl t_CFL_O2]);

%Time Step (h) & # of Time Points
del_t =0.1*del_x/t_CFL;
T_total = 1.5; 
T = round(T_total/del_t);  

%Time to Steady State
T_SS_O2 = 0; 
T_SS_Gl = 0;
T_SS_LA = 0;

%Initial condition
LA = zeros(T,HN);
O2 = CO2_bulk*ones(T, HN); 
Gl = CGl_bulk*ones(T, HN); 

%x = HN case:
O2(:, HN) = CO2_bulk;
Gl(:,HN) = CGl_bulk;
LA(:,HN) = 0;

%Model
for t=2:T
    
    
    for x = 2:(HN-1)
        
        rxn(t,x) = rho(x)*(O2(t,x)/(O2(t,x)+KmO2))*(Gl(t,x)/(Gl(t,x)+KmGl));
        
        diffO2 = del_t*((del_x^-2)*D_O2*(O2(t-1, x+1) + O2(t-1, x-1) - 2*O2(t-1, x)));
        diffGl = del_t*((del_x^-2)*D_Gl*(Gl(t-1, x+1) + Gl(t-1, x-1) - 2*Gl(t-1, x)));
        diffLA = del_t*((del_x^-2)*D_La*(LA(t-1, x+1) + LA(t-1, x-1) - 2*LA(t-1, x)));
        
        
        O2(t, x) = diffO2 - del_t*rxn(t,x)*RO2/YO2 + O2(t-1, x);
        if O2(t,x) < 0
            O2(t,x) = 0;
        end
        
        Gl(t, x) = diffGl - del_t*rxn(t,x)*RGl/YGl + Gl(t-1, x);
        if Gl(t,x) < 0
            Gl(t,x) = 0;
        end
        
        LA(t,x) = diffLA + del_t*rxn(t,x)*RLA/YLA + LA(t-1, x);
        
    end
    
    %x = 1 case:
    O2(t,1) = O2(t,2);
    Gl(t,1) = Gl(t,2);
    LA(t,1) = LA(t,2);
    
    %Calcluate Time to Steady State
    SSO2 = sum(abs(O2(t,:) - O2(t-1,:)));
    if abs(SSO2) < 1e-4 && T_SS_O2 == 0
        T_SS_O2 = round(t*del_t,4);
    end
    
    SSGl = sum(abs(Gl(t,:) - Gl(t-1,:)));
    if abs(SSGl) < 1e-4 && T_SS_Gl == 0
        T_SS_Gl = round(t*del_t,4);
    end
    
    SSLa = sum(abs(LA(t,:) - LA(t-1,:)));
    if abs(SSLa) < 1e-4 && T_SS_LA == 0
        T_SS_LA = round(t*del_t,4);
    end
    
    
end

%Penetrance
O2_pen = find(O2(T,:) ~= 0,1,'first')*del_x;
Gl_pen = find(Gl(T,:) ~= 0,1,'first')*del_x;
LA_pen = find(LA(T,:) == 0,1,'first')*del_x;

%Visualization
figure
pos = del_x.*linspace(1, HN, HN);
plot(pos, O2(T, :), 'm', pos, Gl(T, :), 'c', pos, LA(T,:), 'g')
xlim([0 L+H])
xlabel('Position')
ylabel('Substrate Conc. (g/L)')
legend('Oxygen','Glucose','Lactic Acid', 'Location','northwest')
text(L-200, CGl_bulk, ['O_2 penetrance = ', num2str(O2_pen)])
text(L-200, 0.95*CGl_bulk, ['Gl penetrance = ', num2str(Gl_pen)])
text(L-200, 0.9*CGl_bulk, ['LA penetrance = ', num2str(LA_pen)])
text(L-600, CGl_bulk, ['O_2 Time to SS = ', num2str(T_SS_O2)])
text(L-600, 0.95*CGl_bulk, ['Gl Time to SS = ', num2str(T_SS_Gl)])
text(L-600, 0.9*CGl_bulk, ['LA Time to SS = ', num2str(T_SS_LA)])



%% Sources
%(1)Thomlinson, R. H. & Gray, L. H. (1955) The Histological Structure of Some
% Human Lung Cancers and the Possible Implications for Radiotherapy. British
% journal of cancer 9, 539-549.
%(2)Matoba, Munetaka, et al. “Lung Carcinoma: Diffusion-Weighted MR 
% Imaging—Preliminary Evaluation with Apparent Diffusion Coefficient.” 
% Radiology, vol. 243, no. 2, 2007, pp. 570–577., doi:10.1148/radiol.2432060131.
%(3)Bassi, A. S., Rohani, S., & Macdonald, D. G. (1987) Measurement of effective
% diffusivities of lactose and lactic acid in 3% agarose gel membrane.
% Biotechnology and Bioengineering 30, 794-797.
%(4)Collins, J. A., Rudenski, A., Gibson, J., Howard, L., & O'Driscoll, R. 
%(2015). Relating oxygen partial pressure, saturation and content:
% the haemoglobin-oxygen dissociation curve. Breathe (Sheffield, England), 11(3), 
% 194–201. https://doi.org/10.1183/20734735.001415
%(5)Güemes M, Rahman SA, Hussain K. What is a normal blood glucose? Archives 
% of Disease in Childhood 2016;101:569-574.
%(6)Swarnali Acharyya, Lynn Matrisian, Danny R. Welch, Joan Massagué,
% 18 - Invasion and Metastasis,
% Editor(s): John Mendelsohn, Joe W. Gray, Peter M. Howley, Mark A. Israel, Craig B. Thompson,
% The Molecular Basis of Cancer (Fourth Edition), Content Repository Only!,
% 2015, Pages 269-284.e2, ISBN 9781455740666,
% https://doi.org/10.1016/B978-1-4557-4066-6.00018-4.
% (http://www.sciencedirect.com/science/article/pii/B9781455740666000184)
%(7)Wagner, B. A., Venkataraman, S., & Buettner, G. R. (2011). The rate of 
% oxygen utilization by cells. Free radical biology & medicine, 51(3), 700–712. 
% https://doi.org/10.1016/j.freeradbiomed.2011.05.024
%(8)Glucose transporters and transport kinetics in retinoic acid-differentiated T47D human breast cancer cells
% Dalia Rivenzon-Segal, Edna Rushkin, Sylvie Polak-Charcon, and Hadassa Degani
% American Journal of Physiology-Endocrinology and Metabolism 2000 279:3, E508-E519
% (9)Mathur, D. (2020). Unpublished preliminary data from Seahorse & YSI
% analyzers.
% (10) Gay, R.J. and Hilf, R. (1980), Density?dependent and adaptive 
% regulation of glucose transport in primary cell cultures of the R3230AC rat
% mammary adenocarcinoma. J. Cell. Physiol., 102: 155-174. 
% (11) Rhoades, R A, et al. “Lactate Metabolism in Perfused Rat Lung.” 
% American Journal of Physiology-Endocrinology and Metabolism, vol. 235,
% no. 6, 1978, doi:10.1152/ajpendo.1978.235.6.e619.
% (12) E. Walum, A. Edstrom. (1976), Kinetics of 2-deoxy-d-glucose transport
% into cultured mouse neuroblastoma cells. Experimental Cell Research, vol. 97,
% no. 1: 15-22, ISSN 0014-4827.
% (13) O’Brien, J., Kla, K.M., Hopkins, I.B. et al. Kinetic Parameters and 
% Lactate Dehydrogenase Isozyme Activities Support Possible Lactate Utilization
% by Neurons. Neurochem Res 32, 597–607 (2007). 
