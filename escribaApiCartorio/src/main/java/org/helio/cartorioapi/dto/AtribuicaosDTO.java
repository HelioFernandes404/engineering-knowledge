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
import javax.validation.constraints.Size;


@Data
@AllArgsConstructor
@NoArgsConstructor
public class AtribuicaosDTO {

    @Id
    @NotBlank(message = "ID é obrigatório")
    @Size(max = 20, message = "ID deve ter no máximo 20 caracteres")
    private String id;

    @NotBlank(message = "Nome é obrigatório")
    @Size(max = 50, message = "Nome deve ter no máximo 50 caracteres")
    @Column(unique = true)
    private String nome;

    private boolean situacao = true;

    public AtribuicaosDTO(Atribuicaos entity) {
        id = entity.getId();
        nome = entity.getNome();
        situacao = entity.isSituacao();
    }

}
