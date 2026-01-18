package org.helio.cartorioapi;


import org.helio.cartorioapi.repositorios.CartoriosRepository;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CartorioapiApplication {

    public static void main(String[] args) {
        SpringApplication.run(CartorioapiApplication.class, args);
    }

    @Bean
    public CommandLineRunner mappingDemo(
    ) {
        return args -> {
            /*
            // Create a new SituacaoCartorio and save it
            SituacaoCartorio newSituacao = new SituacaoCartorio("SIT_ATIVO", "Ativo");
            newSituacao = situacaoCartorioRepository.save(newSituacao);

            // Create a new Cartorios and set its situacao to the newly created SituacaoCartorio
            Cartorios cartorios = new Cartorios();
            cartorios.setNome("catorio testes");
            cartorios.setObservacao("Observacao de catorio");
            cartorios.setSituacao(newSituacao); // Ensure this correctly sets the situacao_id to the id of newSituacao

            // Create a new AtribuicaoCartorio and save it
            AtribuicaoCartorio atribuicao = new AtribuicaoCartorio("ID123", "Nome do Cartório", true);
            atribuicao = atribuicaoCartorioRepository.save(atribuicao);

            // Add the AtribuicaoCartorio to the Cartorios
            List<AtribuicaoCartorio> list = new ArrayList<>();
            list.add(atribuicao);
            cartorios.setAtribuicoes(list);

            // Save the Cartorios
            cartoriosRepository.save(cartorios);

             */
        };
    }
}
