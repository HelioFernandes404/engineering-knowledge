package org.helio.cartorioapi.entidades;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Set;

@Data
@AllArgsConstructor
@NoArgsConstructor

@Entity
@Table(name = "tb_cartorios")
public class Cartorios {

    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    private Integer id;

    @Size(max = 150, message = "Nome deve ter no máximo 50 caracteres")
    @NotBlank(message = "Nome é obrigatório")
    @Column(unique = true)
    private String nome;

    @Column(length = 250)
    private String observacao;

    @ManyToOne
    @JoinColumn(name = "situacao_id", referencedColumnName = "id")
    private Situacaos situacao;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
            name = "cartorio_atribuicao",
            joinColumns = @JoinColumn(name = "cartorio_id"),
            inverseJoinColumns = @JoinColumn(name = "atribuicao_id")
    )
    @JsonManagedReference
    private List<Atribuicaos> atribuicoes;
}
