package org.helio.cartorioapi.services;
import org.helio.cartorioapi.dto.SituacaosDTO;
import org.helio.cartorioapi.dto.AtribuicaosMinDTO;
import org.helio.cartorioapi.dto.SituacaosDTO;
import org.helio.cartorioapi.dto.SituacaosMinDTO;
import org.helio.cartorioapi.entidades.Atribuicaos;
import org.helio.cartorioapi.entidades.Situacaos;
import org.helio.cartorioapi.entidades.Situacaos;
import org.helio.cartorioapi.repositorios.SituacaoRepository;
import org.helio.cartorioapi.services.exceptions.DatabaseException;
import org.helio.cartorioapi.services.exceptions.ResourceNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityNotFoundException;
import java.util.Optional;

@Service
public class SituacaosServices {

    @Autowired
    private SituacaoRepository repository;


    @Transactional(readOnly = true)
    public Page<SituacaosMinDTO> findAll(Pageable pageable) {
        Page<Situacaos> result = repository.findAllBy(pageable);
        return result.map(x -> new SituacaosMinDTO(x));
    }

    @Transactional(readOnly = true)
    public SituacaosDTO findById(String id) {
        Situacaos entity = repository.findById(id).orElseThrow(
                () -> new ResourceNotFoundException("Recurso não encontrado"));
        return new SituacaosDTO(entity);
    }

    @Transactional
    public SituacaosDTO insert(SituacaosDTO dto) {
        Optional<Situacaos> existingById = repository.findById(dto.getId());
        if (existingById.isPresent()) {
            throw new DatabaseException("Registro já cadastrado");
        }

        Optional<Situacaos> existingByNome = repository.findByNome(dto.getNome());
        if (existingByNome.isPresent()) {
            throw new DatabaseException("Nome já informado no registro com código: " + existingByNome.get().getId());
        }


        Situacaos entity = new Situacaos();
        copyDtoToEntity(dto, entity);
        entity = repository.save(entity);
        return new SituacaosDTO(entity);
    }


    @Transactional
    public SituacaosDTO update(String id, SituacaosDTO dto) {
        Optional<Situacaos> existing = repository.findById(id);
        if (!existing.isPresent()) {
            throw new DatabaseException("Registro com ID " + id + " não encontrado");
        }
        Situacaos entity = existing.get();
        if (!entity.getNome().equals(dto.getNome())) {
            Optional<Situacaos> duplicate = repository.findByNome(dto.getNome());
            if (duplicate.isPresent()) {
                throw new DatabaseException("Nome já informado no registro com código " + duplicate.get().getId());
            }
        }
        entity.setId(dto.getId());
        entity.setNome(dto.getNome());
        entity = repository.save(entity);
        return new SituacaosDTO(entity);
    }

    @Transactional(propagation = Propagation.SUPPORTS)
    public void delete(String id) {
        try {
            repository.deleteById(id);
        } catch (EmptyResultDataAccessException e) {
            throw new ResourceNotFoundException("Recurso não encontrado");
        } catch (DataIntegrityViolationException e) {
            throw new DatabaseException("Registro utilizado em outro cadastro");
        }
    }

    private void copyDtoToEntity(SituacaosDTO dto, Situacaos entity) {
        entity.setId(dto.getId());
        entity.setNome(dto.getNome());
    }
}
