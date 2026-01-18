package org.helio.cartorioapi.repositorios;

import org.helio.cartorioapi.entidades.Atribuicaos;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;


@Repository
public interface AtribuicaoRepository extends JpaRepository<Atribuicaos, String> {
    Page<Atribuicaos> findAllBy(Pageable pageable);

    Atribuicaos getReferenceById(String id);
    boolean existsByNome(String nome);
    boolean existsById(String id);
    @Query("SELECT a FROM Atribuicaos a WHERE a.nome = :nome")
    Optional<Atribuicaos> findByNome(@Param("nome") String nome);
}
