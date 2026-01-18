package org.helio.cartorioapi.entidades;
import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.helio.cartorioapi.dto.SituacaosDTO;

import java.util.List;
import java.util.Set;

@Data
@AllArgsConstructor
@NoArgsConstructor

@Entity
@Table(name = "tb_situacaos")
public class Situacaos {

    @Size(max = 20, message = "ID deve ter no máximo 20 caracteres")
    @NotBlank(message = "ID é obrigatório")
    @Id
    private String id;

    @Size(max = 50, message = "Nome deve ter no máximo 50 caracteres")
    @NotBlank(message = "Nome é obrigatório")
    @Column(unique = true)
    private String nome;

    @OneToMany(mappedBy = "situacao")
    @JsonBackReference // Adicionado para evitar serialização circular
    private List<Cartorios> cartorios;

    public Situacaos(SituacaosDTO situacaosDTO) {
        id = situacaosDTO.getId();
        nome = situacaosDTO.getNome();
    }
}

