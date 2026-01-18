package org.helio.cartorioapi.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.helio.cartorioapi.entidades.Atribuicaos;
import org.helio.cartorioapi.entidades.Cartorios;


import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;


@Data
@AllArgsConstructor
@NoArgsConstructor
public class CartoriosDTO {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @NotBlank(message = "Nome é obrigatório")
    @Size(max = 150, message = "Nome deve ter no máximo 50 caracteres")
    @Column(unique = true)
    private String nome;

    @Size(max = 250)
    private String observacao;

    @NotNull
    private SituacaosDTO situacao;

    @NotEmpty
    private List<AtribuicaosDTO> atribuicoes;

    public CartoriosDTO(Cartorios entity) {
        this.id = entity.getId();
        this.nome = entity.getNome();
        this.observacao = entity.getObservacao();
        this.situacao = new SituacaosDTO(entity.getSituacao());
        this.atribuicoes = entity.getAtribuicoes().stream()
                .map(AtribuicaosDTO::new)
                .collect(Collectors.toList());
    }
}
