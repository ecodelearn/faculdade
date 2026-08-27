    (async function baixarTudo() {                                                                                                                                                                       
      console.log("🚀 Iniciando extração e download dos materiais...");                                                                                                                                  
                                                                                                                                                                                                         
      const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));                                                                                                                             
                                                                                                                                                                                                         
      // 1. Localizar todos os botões de materiais                                                                                                                                                       
      const botoesPdf = Array.from(document.querySelectorAll('button')).filter(b =>                                                                                                                      
        b.innerText.includes('Download') && b.querySelector('.fa-arrow-down-to-line')                                                                                                                    
      );                                                                                                                                                                                                 
      const botoesSlides = Array.from(document.querySelectorAll('.fa-presentation-screen')).map(i => i.closest('button')).filter(Boolean);                                                               
      const botoesAudios = Array.from(document.querySelectorAll('.fa-volume')).map(i => i.closest('button')).filter(Boolean);                                                                            
      const botoesLegendas = Array.from(document.querySelectorAll('.fa-bars-staggered')).map(i => i.closest('button')).filter(Boolean);                                                                  
                                                                                                                                                                                                         
      console.log(`📦 Encontrados:`);
      console.log(`   - ${botoesPdf.length} PDFs de Matéria / Apostilas`);
      console.log(`   - ${botoesSlides.length} PDFs de Slides`);
      console.log(`   - ${botoesAudios.length} Áudios de Videoaulas`);
      console.log(`   - ${botoesLegendas.length} Legendas SRT`);
  
      // Junta todos com intervalo de 1.5s entre cada download para não travar o navegador
      const todosBotoes = [
        ...botoesPdf.map(b => ({ tipo: 'PDF Matéria', btn: b })),
        ...botoesSlides.map(b => ({ tipo: 'Slide', btn: b })),
        ...botoesLegendas.map(b => ({ tipo: 'Legenda', btn: b })),
        ...botoesAudios.map(b => ({ tipo: 'Áudio', btn: b }))
      ];
  
      console.log(`⏳ Total de ${todosBotoes.length} downloads a realizar...`);
  
      for (let i = 0; i < todosBotoes.length; i++) {
        const item = todosBotoes[i];
        console.log(`[${i + 1}/${todosBotoes.length}] Baixando ${item.tipo}...`);
        try {
          item.btn.click();
        } catch (e) {
          console.warn("Erro ao clicar no botão:", e);
        }
        await sleep(1500); // aguarda 1.5 segundos
      }
  
      console.log("🎉 Todos os downloads foram solicitados com sucesso!");
    })();
