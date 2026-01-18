package org.helio.cartorioapi.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.helio.cartorioapi.entidades.Atribuicaos;

import javax.persistence.Column;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.validation.constraints.NotBlank;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AtribuicaosMinDTO {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id;

    @Column(length = 50)
    @NotBlank(message = "Campo requerido")
    private String nome;

    // Construtor de cópia para a classe SituacaoCartorioDTO.
    public AtribuicaosMinDTO(Atribuicaos entity) {
        id = entity.getId();
        nome = entity.getNome();
    }
}
