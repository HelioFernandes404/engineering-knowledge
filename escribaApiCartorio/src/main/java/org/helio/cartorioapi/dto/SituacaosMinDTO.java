package org.helio.cartorioapi.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.helio.cartorioapi.entidades.Situacaos;

import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SituacaosMinDTO {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id;
    private String nome;


    // Construtor de cópia para a classe SituacaoCartorioDTO.
    public SituacaosMinDTO(Situacaos entity) {
        id = entity.getId();
        nome = entity.getNome();
    }

}
