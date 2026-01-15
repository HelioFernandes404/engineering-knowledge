package org.helio.cartorioapi.repositorios;


import org.helio.cartorioapi.entidades.Atribuicaos;
import org.helio.cartorioapi.entidades.Situacaos;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SituacaoRepository extends JpaRepository<Situacaos, String> {
    Page<Situacaos> findAllBy(Pageable pageable);

    Situacaos getReferenceById(String id);
    boolean existsByNome(String nome);
    boolean existsById(String id);
    @Query("SELECT a FROM Situacaos a WHERE a.nome = :nome")
    Optional<Situacaos> findByNome(@Param("nome") String nome);
}

