package org.helio.cartorioapi.repositorios;

import org.helio.cartorioapi.entidades.Cartorios;
import org.helio.cartorioapi.entidades.Cartorios;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CartoriosRepository extends JpaRepository<Cartorios, Integer> {

    @Query(value = "SELECT c.id AS cartorio_id, c.nome AS cartorio_nome, c.observacao AS cartorio_observacao, s.id AS situacao_id, s.nome AS situacao_nome, GROUP_CONCAT(a.nome) AS atribuicoes FROM tb_cartorios c JOIN tb_situacaos s ON c.situacao_id = s.id JOIN cartorio_atribuicao ca ON c.id = ca.cartorio_id JOIN tb_atribuicaos a ON ca.atribuicao_id = a.id GROUP BY c.id, c.nome, c.observacao, s.id, s.nome HAVING COUNT(a.id) >=0", nativeQuery = true)
    List<Object[]> findCartoriosWithAtribuicoes();

    Page<Cartorios> findAllBy(Pageable pageable);

    Cartorios getReferenceById(Integer id);

    Cartorios getReferenceById(String id);
    boolean existsByNome(String nome);
    boolean existsById(String id);
    @Query("SELECT a FROM Cartorios a WHERE a.nome = :nome")
    Optional<Cartorios> findByNome(@Param("nome") String nome);
}
